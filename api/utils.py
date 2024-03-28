import sqlite3
import pandas as pd
from numpy import dtype
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import recall_score, accuracy_score, f1_score
import pickle
import json

from database.core import DBToPredict, DBPrediction
from database.prediction import SinglePredictionOutput

def predict_single(model_name, order):

    with open(f"ml_models/{model_name}.pkl", 'rb') as file:
        loaded_model = pickle.load(file)

    data = {'produit_recu':[order.produit_recu],
            'temps_livraison':[order.temps_livraison]}
    df_to_predict = pd.DataFrame(data)

    prediction = loaded_model.predict(df_to_predict)

    return prediction[0]

def update_model_name(model_name):
    data = {
    "model_name": model_name
    }
    # Writing dictionary to a JSON file
    with open("model_name.json", "w") as json_file:
        json.dump(data, json_file)

def get_model_name():
    with open("model_name.json", "r") as json_file:
        data = json.load(json_file)
    return data["model_name"]

def get_db(db_name = "olist.db"):
    connection = sqlite3.connect(db_name)
    df_reviews = pd.read_sql_query("SELECT * FROM Reviews",connection)
    return df_reviews , connection

def clean_data(df_reviews, connection):
    df_reviews = df_reviews.drop(["timestamp_field_7"],axis=1)

    if df_reviews.shape[1]!= 7:
        raise ValueError("Le nombre de colonnes ne correspond pas")
    else:
        print("Valeurs manquantes: OK")

    # Gestion des doublons
    df_reviews = df_reviews.drop_duplicates(['order_id','review_score','review_comment_title','review_comment_message','review_creation_date'])


    # Changement des types
    df_reviews.review_creation_date = pd.to_datetime(df_reviews['review_creation_date'], format= '%Y-%m-%d %H:%M:%S', errors="coerce")
    df_reviews.review_answer_timestamp = pd.to_datetime(df_reviews['review_answer_timestamp'], format= '%Y-%m-%d %H:%M:%S', errors="coerce")




    if df_reviews.dtypes['review_creation_date'] != dtype('<M8[ns]') or df_reviews.dtypes['review_answer_timestamp'] != dtype('<M8[ns]'):
        raise ValueError("Les dates ne sont pas au bon format")
    else:
        print("Gestion des dates: OK")

    #Changement des valeurs types pour les dates
    df_reviews = df_reviews.dropna(subset=['review_creation_date','review_answer_timestamp'])

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

    # Création des variables montant price et freight value

    df_order_item = pd.read_sql_query("SELECT * FROM OrderItem",connection)

    df_montant_global = df_order_item[["order_id","price","freight_value"]].groupby("order_id").sum()

    df = df.merge(df_montant_global, how='left', on ='order_id')

    print("Création de total_price et total_freight_value")

    # Récupération des variables description, photo

    df_products = pd.read_sql_query("SELECT * FROM Products",connection)

    df_item_product = df_order_item[['order_id','product_id']].merge(df_products, how='left', on ='product_id')
    df_item_product["product_photos_qty"] = df_item_product["product_photos_qty"].replace("","0").astype("int")
    df_item_product["product_description_lenght"] = df_item_product["product_description_lenght"].replace("","0").astype("int")

    df_item_product_group_by = df_item_product[['order_id','product_photos_qty','product_description_lenght']].groupby('order_id').mean()


    df_item_product_group_by = df_item_product_group_by.reset_index()

    df = df.merge(df_item_product_group_by,how='left')

    return df

def feature_engineering(df):
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
    return df

def modelisation(df, model_name):
    df = df.dropna()
    y = df['score']
    X = df[["produit_recu","temps_livraison"]]
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, random_state=42)

    model = LogisticRegression()

    model.fit(X_train,y_train)


    recall_train = round(recall_score(y_train, model.predict(X_train)),4)
    acc_train = round(accuracy_score(y_train, model.predict(X_train)),4)
    f1_train = round(f1_score(y_train, model.predict(X_train)),4)

    print(f"Pour le jeu d'entrainement: \n le recall est de {recall_train}, \n l'accuracy de {acc_train} \n le f1 score de {f1_train}")

    recall_test = round(recall_score(y_test, model.predict(X_test)),4)
    acc_test = round(accuracy_score(y_test, model.predict(X_test)),4)
    f1_test = round(f1_score(y_test, model.predict(X_test)),4)

    print(f"['{model_name}', {recall_train}, {acc_train}, {f1_train}, {recall_test}, {acc_test}, {f1_test} ],")

    # Save the model to a file using pickle
    with open(f"ml_models/{model_name}.pkl", 'wb') as file:
        pickle.dump(model, file)
    
    return {
        "model_name": model_name,
        "recall_train": recall_train,
        "acc_train": acc_train,
        "f1_train": f1_train,
        "recall_test": recall_test,
        "acc_test": acc_test,
        "f1_test": f1_test
    }

def train(model_name): 
    df_reviews, connection = get_db()
    df_clean = clean_data(df_reviews, connection)
    df = feature_engineering(df_clean)
    metrics_dict = modelisation(df, model_name)
    connection.close()
    return  metrics_dict 

###############################################################################
def make_predictions(model_name, session):
    try:
        entries_to_predict = session.query(DBToPredict).all()
        for entry in entries_to_predict:
            model_name = get_model_name()
            prediction = predict_single(model_name, entry)
            prediction = SinglePredictionOutput(prediction=prediction)
            new_prediction = DBPrediction(id=entry.id, prediction=prediction)
            session.add(new_prediction)
        session.commit()
    finally:
        session.close()    
##############################################################################



