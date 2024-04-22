
def training(run_name,start_date="2017-01-01",end_date="2018-01-01"):
    
    from data_cleaning import data_cleaning
    from feature_engineering import feature_engineering
    from modelisation import modelisation
    import sqlite3

    connection = sqlite3.connect("olist.db")
    data_cleaning(connection,run_name,start_date,end_date)
    feature_engineering(connection,run_name)
    modelisation(connection,run_name)