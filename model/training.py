from .data_cleaning import data_cleaning
from .feature_engineering import feature_engineering
from .modelisation import modelisation
from .utils import connect_to_postgres
import sqlite3

def training(run_name,start_date="2017-01-01",end_date="2018-01-01"):
    

    connection = connect_to_postgres()
    df_clean = data_cleaning(connection,run_name,start_date,end_date)
    print(df_clean.head())
    df_clean.to_sql(run_name +'_cleandataset', connection, index=False, if_exists='replace')
    
    df_feat = feature_engineering(connection,run_name)
    df_feat.to_sql(run_name +'_trainingdataset', connection, index=False, if_exists='replace')
    
    run_id = modelisation(connection,run_name)
    return run_id