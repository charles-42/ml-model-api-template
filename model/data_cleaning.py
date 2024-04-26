import pandas as pd
import sqlite3
import numpy as np


def data_cleaning(connection,run_name, start_date="2017-01-01",end_date="2018-01-01"):
    from numpy import dtype
    
    review_query = """
    SELECT order_id, review_score, review_creation_date 
    FROM Reviews
    """
    
    df_reviews = pd.read_sql_query(review_query, connection)

    # Gestion des doublons
    df_reviews = df_reviews.drop_duplicates()

    # Gestion des valeurs manquantes
    df_reviews = df_reviews.dropna(subset=['order_id','review_score','review_creation_date'])

    # Changement des types
    df_reviews.review_creation_date = pd.to_datetime(df_reviews['review_creation_date'], format= '%Y-%m-%d %H:%M:%S', errors="coerce")

    # Filter reviews between start_date and end_date
    df_reviews = df_reviews[(df_reviews.review_creation_date >= start_date) & (df_reviews.review_creation_date <= end_date)] 

    order_query = """
    SELECT order_id, order_purchase_timestamp, order_delivered_customer_date, 
           order_estimated_delivery_date 
    FROM Orders
    """

    df_orders = pd.read_sql_query(order_query,connection)

    df = df_reviews.merge(df_orders, how='left', on ='order_id')


    # Gestion des types de data
    df.order_purchase_timestamp = pd.to_datetime(df['order_purchase_timestamp'], 
                                                format= '%Y-%m-%d %H:%M:%S', 
                                                errors="coerce")

    df.order_delivered_customer_date = pd.to_datetime(df['order_delivered_customer_date'], 
                                                    format= '%Y-%m-%d %H:%M:%S', 
                                                    errors="coerce")

    df.order_estimated_delivery_date = pd.to_datetime(df['order_estimated_delivery_date'], 
                                                    format= '%Y-%m-%d %H:%M:%S', 
                                                    errors="coerce")
    
    df = df.dropna()
    
    return df
    




if __name__ == "__main__":
    connection = sqlite3.connect("olist.db")
    df = data_cleaning(connection,"first_run_2017",start_date="2017-01-01",end_date="2018-01-01")
    df.to_sql("first_run_2017" +'_CleanDataset', connection, index=False, if_exists='replace')
    