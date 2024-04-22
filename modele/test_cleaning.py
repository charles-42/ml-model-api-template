import pytest
import pandas as pd
from data_cleaning import cleaning_review, data_cleaning  # Import your function from the module where it's defined
from unittest.mock import patch  # Import patch from unittest.mock
import numpy as np
import sqlite3

# Mocking the connection
class MockConnection:
    def __init__(self):
        # Define your mock data here or use libraries like pytest-mock to mock the behavior
        pass

@pytest.fixture
def connection():
    return MockConnection()

def test_cleaning_review(connection):
    # Create some mock data for testing
    mock_data = pd.DataFrame({
        'review_id': [0, 1, 2, 3, 3, 4],
        'order_id': [0, 1, 2, 3, 3, 4],
        'review_score': [1, 4, 5, 3, 3, 4],
        'review_comment_title': ['Title 0','Title 1', 'Title 2', 'Title 3', 'Title 3', 'Title 4'],
        'review_comment_message': ['Message 0','Message 1', 'Message 2', 'Message 3',  'Message 3', 'Message 4'],
        'review_creation_date': ['2016-01-01 12:00:00','2017-01-01 12:00:00', '2017-01-02 12:00:00', '2017-01-03 12:00:00',  '2017-01-03 12:00:00', np.nan],
        'review_answer_timestamp': ['2016-01-02 12:00:00','2017-01-02 12:00:00', '2017-01-03 12:00:00', '2017-01-04 12:00:00', '2017-01-04 12:00:00', '2017-01-04 12:00:00'],
        'timestamp_field_7': [0, 1, 2, 3, 3, 4]
    })

    # Mocking the SQL query execution
    def mock_read_sql_query(query, connection):
        return mock_data

    with patch('pandas.read_sql_query', side_effect=mock_read_sql_query):
        cleaned_data = cleaning_review(connection, "2017-01-01","2018-01-01")

    # Write assertions to check if the cleaning process works as expected
    assert len(cleaned_data) == 3  # Check if the number of rows is correct after cleaning
    assert set(cleaned_data.columns) == {'review_id', 'order_id', 'review_score', 'review_comment_title', 'review_comment_message', 'review_creation_date', 'review_answer_timestamp'}  # Check if all expected columns are present

    # Assert that there are no raw before the start_date
    assert cleaned_data['review_creation_date'].min() >= pd.to_datetime('2017-01-01')

    # Add more assertions to check specific cleaning steps based on your function's logic
    # For example, you can check if the date format conversion is correct
    assert cleaned_data['review_creation_date'].dtype == '<M8[ns]'
    assert cleaned_data['review_answer_timestamp'].dtype == '<M8[ns]'


# TEST DATA_CLEANING FUNCTION
# On teste sur la base de prod, c'est pas optimisé
def test_cleaning_data():
    connection_real_db = sqlite3.connect("olist.db")
    data_cleaning(connection_real_db,"test_run", start_date="2017-01-01",end_date="2018-01-01")
    df_cleaned = pd.read_sql_query("SELECT * FROM test_run_CleanDataset",connection_real_db)
    target_columns = [
       'review_id', 'order_id', 'review_score', 'review_comment_title',
       'review_comment_message', 'review_creation_date',
       'review_answer_timestamp', 'customer_id', 'order_status',
       'order_purchase_timestamp', 'order_approved_at',
       'order_delivered_carrier_date', 'order_delivered_customer_date',
       'order_estimated_delivery_date', 'price', 'freight_value',
       'product_photos_qty', 'product_description_lenght']
    for col in target_columns:
        assert col in df_cleaned.columns

    connection_real_db.close()