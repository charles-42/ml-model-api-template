def feature_engineering(connection,run_name):
    import pandas as pd
    import sqlite3

    df = pd.read_sql_query(f"SELECT * FROM {run_name}_CleanDataset",connection)

    df.review_creation_date = pd.to_datetime(df['review_creation_date'], 
                                             format= '%Y-%m-%d %H:%M:%S', 
                                             errors="coerce")

    df.review_answer_timestamp = pd.to_datetime(df['review_answer_timestamp'], 
                                                format= '%Y-%m-%d %H:%M:%S', 
                                                errors="coerce")


    df.order_purchase_timestamp = pd.to_datetime(df['order_purchase_timestamp'], 
                                            format= '%Y-%m-%d %H:%M:%S', 
                                            errors="coerce")

    df.order_delivered_customer_date = pd.to_datetime(df['order_delivered_customer_date'], 
                                                    format= '%Y-%m-%d %H:%M:%S', 
                                                    errors="coerce")

    df.order_estimated_delivery_date = pd.to_datetime(df['order_estimated_delivery_date'], 
                                                    format= '%Y-%m-%d %H:%M:%S', 
                                                    errors="coerce")
    

    # Creation de la variable score
    df['score'] = df['review_score'].apply(lambda x : 1 if x==5 else 0)
    df["temps_livraison"] = (df.order_delivered_customer_date - df.order_purchase_timestamp).dt.days
    df["retard_livraison"] = (df.order_delivered_customer_date - df.order_estimated_delivery_date).dt.days

    def f(x):
        (delivered_date,review_date)=x
        if pd.isna(delivered_date):
            return 0
        elif delivered_date.normalize()>review_date:
            return 0
        else:
            return 1

    df['produit_recu'] = df[["order_delivered_customer_date","review_creation_date"]].apply(f, axis=1)

    df["order_status"] = df["order_status"].apply(lambda x: "unavailable" if x in ["created","approved"] else x)


    df.to_sql(run_name+'_TrainingDataset', connection, index=False, if_exists='replace')
