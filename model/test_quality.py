import pytest
import pandas as pd
from data_cleaning import data_cleaning
from feature_engineering import feature_engineering
from modelisation import modelisation
from unittest.mock import patch  # Import patch from unittest.mock
import mlflow

def pytest_addoption(parser):
    parser.addoption("--run_name", action="store", default="test_run")
    parser.addoption("--start_date", action="store", default="2017-01-01")
    parser.addoption("--end_date", action="store", default="2018-01-01")

@pytest.fixture
def run_name(request):
    return request.config.getoption("--run_name")

@pytest.fixture
def start_date(request):
    return request.config.getoption("--start_date")

@pytest.fixture
def end_date(request):
    return request.config.getoption("--end_date")

@pytest.fixture
def connection(run_name):
    if run_name == 'test_run':
        # Create a mock connection
        class MockConnection:
            def __init__(self):
                self.mock_reviews_data = pd.DataFrame({
                    'order_id': [0, 1, 2, 3, 3, 4],
                    'review_score': [1, 4, 5, 3, 3, 4],
                    'review_creation_date': ['2016-01-01 12:00:00','2017-01-01 12:00:00', '2017-01-02 12:00:00', '2017-01-03 12:00:00',  '2017-01-03 12:00:00', pd.NaT],
                })

                # Mock data for the "orders" table
                self.mock_orders_data = pd.DataFrame({
                    'order_id': [0, 1, 2, 3, 4],
                    'order_purchase_timestamp': ['2016-01-01 12:00:00', '2016-01-02 12:00:00', '2016-01-03 12:00:00', '2016-01-04 12:00:00', '2016-01-05 12:00:00'],
                    'order_delivered_customer_date': ['2016-01-05 12:00:00', '2016-01-07 12:00:00', '2016-01-09 12:00:00', '2016-01-11 12:00:00', '2016-01-12 12:00:00'],
                    'order_estimated_delivery_date': ['2016-01-07', '2016-01-09', '2016-01-11', '2016-01-13', '2016-01-14']
                })

                self.mock_clean_data = pd.DataFrame({
                    'order_id': [1, 2, 3],
                    'review_score': [4, 5, 3],
                    'review_creation_date': ['2017-01-01 12:00:00', '2017-01-02 12:00:00', '2017-01-03 12:00:00'],
                    'order_purchase_timestamp': [ '2016-01-02 12:00:00', '2016-01-03 12:00:00', '2016-01-04 12:00:00'],
                    'order_delivered_customer_date': [ '2016-01-07 12:00:00', '2016-01-09 12:00:00', '2016-01-11 12:00:00'],
                    'order_estimated_delivery_date': [ '2016-01-09', '2016-01-11', '2016-01-13']
                })

                self.mock_training_data = pd.DataFrame({
                    'score': [0, 1, 1, 0, 0],
                    'produit_recu': [1, 1, 0, 0, 1],
                    'temps_livraison': [2, 3, 1, 4, 2]
                })

        return MockConnection()
    else:
        # Create a real connection
        import sqlite3
        connection = sqlite3.connect("olist.db")
        return connection
    

def test_data_cleaning(connection,run_name, start_date, end_date):

    if run_name == 'test_run':
            # Mocking the SQL query execution
        def mock_read_sql_query(query, connection):
            if 'ORDERS' in query:
                return connection.mock_orders_data
            elif 'REVIEWS' in query:
                return connection.mock_reviews_data


        with patch('pandas.read_sql_query', side_effect=mock_read_sql_query):
            df_clean = data_cleaning(connection,run_name, start_date, end_date)

        assert len(df_clean) == 3
    else:
        df_clean = pd.read_sql_query(f"SELECT * FROM {run_name}_CleanDataset",connection)
        df_clean.review_creation_date = pd.to_datetime(df_clean['review_creation_date'])

    
    assert set(df_clean.columns) == {'order_id', 'review_score','review_creation_date',
                                     'order_purchase_timestamp','order_delivered_customer_date','order_estimated_delivery_date'}  # Check if all expected columns are present

    # Assert that there are no raw before the start_date
    assert df_clean['review_creation_date'].min() >= pd.to_datetime(start_date)
    assert df_clean['review_creation_date'].max() <= pd.to_datetime(end_date)

    # Add more assertions to check specific cleaning steps based on your function's logic
    # For example, you can check if the date format conversion is correct
    assert df_clean['review_creation_date'].dtype == '<M8[ns]'
    
    assert not df_clean[['order_id', 'review_score','review_creation_date']].isnull().values.any(), "DataFrame contains missing values"

    # Check for duplicated rows
    assert not df_clean.duplicated().any(), "DataFrame contains duplicated rows"

def test_feature_engineering(connection,run_name):

    if run_name == 'test_run':
            # Mocking the SQL query execution
        def mock_read_sql_query(query, connection):
            return connection.mock_clean_data
        
        with patch('pandas.read_sql_query', side_effect=mock_read_sql_query):
            df_feat = feature_engineering(connection,run_name)
    else:
        df_feat = pd.read_sql_query(f"SELECT * FROM {run_name}_TrainingDataset",connection)

    assert set(df_feat.columns) == {'order_id', 'review_score','review_creation_date',
                                     'order_purchase_timestamp','order_delivered_customer_date','order_estimated_delivery_date',
                                     'score', 'temps_livraison', 'produit_recu', 'retard_livraison'
                                     }  # Check if all expected columns are present

    assert df_feat['score'].isin([0, 1]).all()
    assert df_feat['produit_recu'].isin([0, 1]).all()
    assert df_feat['temps_livraison'].dtype in [int, 'int64'], f"Column 'temps_livraison' is not of integer type"


def test_modelisation(connection,run_name):
    import pickle
    import os
    from sklearn.linear_model import LogisticRegression
    if run_name == 'test_run':
            # Mocking the SQL query execution
        def mock_read_sql_query(query, connection):
            return connection.mock_training_data
        
        with patch('pandas.read_sql_query', side_effect=mock_read_sql_query):
            run_id = modelisation(connection,run_name)
    else:
        experiment = mlflow.get_experiment_by_name("predict_review_score")
        runs = mlflow.search_runs(experiment_ids=experiment.experiment_id)
        # Filter runs by run name
        filtered_runs = runs[runs['tags.mlflow.runName'] == run_name]
        run_id = filtered_runs.iloc[0]['run_id']

    
    assert run_id 
    run = mlflow.get_run(run_id)
    assert run
    # Get run metrics
    metrics = run.data.metrics
    assert set(metrics.keys()) == {'accuracy_test', 'accuracy_train', 'f1_test', 'f1_train','recall_train','recall_test'}
    

    if run_name != 'test_run':
        # test for accuracy
        assert metrics['accuracy_test'] > 0.6
        # test for overfitting
        assert metrics['accuracy_train']- metrics['accuracy_test'] < 0.2

    artifact_uri = run.info.artifact_uri

    # Construct the path to the model pickle file within the artifacts directory
    modelel_pickle_path = os.path.join(artifact_uri.replace("file://", ""), run_name, "model.pkl")

    with open(modelel_pickle_path, 'rb') as f:
        model = pickle.load(f)
        assert type(model) == LogisticRegression
    
    if run_name == 'test_run':
        mlflow.delete_run(run_id)