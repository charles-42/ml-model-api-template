import pandas as pd
import sqlite3
import numpy as np


def cleaning_review(connection,start_date="2017-01-01",end_date="2018-01-01"):
    from numpy import dtype
    df_reviews = pd.read_sql_query("SELECT * FROM Reviews",connection)


    # Gestion valeurs manquantes
    df_reviews = df_reviews.drop(["timestamp_field_7"],axis=1)

    # Gestion des doublons
    df_reviews = df_reviews.drop_duplicates(['order_id','review_score','review_comment_title','review_comment_message','review_creation_date'])


    # Changement des types
    df_reviews.review_creation_date = pd.to_datetime(df_reviews['review_creation_date'], format= '%Y-%m-%d %H:%M:%S', errors="coerce")

    # Filter reviews between start_date and end_date
    df_reviews = df_reviews[(df_reviews.review_creation_date >= start_date) & (df_reviews.review_creation_date <= end_date)] 

    df_reviews.review_answer_timestamp = pd.to_datetime(df_reviews['review_answer_timestamp'], format= '%Y-%m-%d %H:%M:%S', errors="coerce")

    #Changement des valeurs types pour les dates
    df_reviews = df_reviews.dropna(subset=['review_creation_date','review_answer_timestamp'])

    return df_reviews

def cleaning_orders(connection,df_reviews):
    from numpy import dtype
    # Jointure avec la Table Orders
    df_orders = pd.read_sql_query("SELECT * FROM Orders",connection)
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


    if df.dtypes['order_estimated_delivery_date'] != dtype('<M8[ns]') \
        or df.dtypes['order_delivered_customer_date'] != dtype('<M8[ns]')\
        or df.dtypes['order_estimated_delivery_date'] != dtype('<M8[ns]')    :
        raise ValueError("Les dates ne sont pas au bon format")
    else:
        print("Gestion des dates (Orders): OK")
    
    return df

def cleaning_order_item(connection,df_order):
    from numpy import dtype
    # Création des variables montant price et freight value

    df_order_item = pd.read_sql_query("SELECT * FROM OrderItem",connection)

    df_montant_global = df_order_item[["order_id","price","freight_value"]].groupby("order_id").sum()

    df = df_order.merge(df_montant_global, how='left', on ='order_id')

    print("Création de total_price et total_freight_value")
    return df, df_order_item

def cleaning_product(connection,df_order,df_order_item):
    from numpy import dtype
    # Récupération des variables description, photo

    df_products = pd.read_sql_query("SELECT * FROM Products",connection)

    df_item_product = df_order_item[['order_id','product_id']].merge(df_products, how='left', on ='product_id')
    df_item_product["product_photos_qty"] = df_item_product["product_photos_qty"].replace("","0").astype("int")
    df_item_product["product_description_lenght"] = df_item_product["product_description_lenght"].replace("","0").astype("int")

    df_item_product_group_by = df_item_product[['order_id','product_photos_qty','product_description_lenght']].groupby('order_id').mean()


    df_item_product_group_by = df_item_product_group_by.reset_index()

    df = df_order.merge(df_item_product_group_by,how='left')
    return df

def data_cleaning(connection,run_name, start_date="2017-01-01",end_date="2018-01-01"):
    from numpy import dtype
    import pandas as pd
    import sqlite3
    import numpy as np

    df_reviews = cleaning_review(connection)
    
    df_orders = cleaning_orders(connection,df_reviews)

    df_orders, df_order_item = cleaning_order_item(connection,df_orders)
    
    df_orders = cleaning_product(connection,df_orders, df_order_item)

    df_orders.to_sql(run_name +'_CleanDataset', connection, index=False, if_exists='replace')



if __name__ == "__main__":
    connection = sqlite3.connect("olist.db")
    df = data_cleaning(connection,"first_run_2017",start_date="2017-01-01",end_date="2018-01-01")
