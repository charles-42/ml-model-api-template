from feature_engineering import feature_engineering
import sqlite3
import pandas as pd

def test_cleaning_data():
    connection = sqlite3.connect("olist.db")
    feature_engineering(connection,"test_run")
    df_feat = pd.read_sql_query("SELECT * FROM test_run_TrainingDataset",connection)
    target_columns = ['score', 'temps_livraison', 'retard_livraison','produit_recu']
    for col in target_columns:
        assert col in df_feat.columns

    connection.close()
