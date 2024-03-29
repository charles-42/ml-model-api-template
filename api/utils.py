import sqlite3
import pandas as pd
from numpy import dtype
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import recall_score, accuracy_score, f1_score
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType
import onnxruntime as rt
import json

import os
if not os.path.exists('ml_models'):
    os.makedirs('ml_models')
    
    

def predict_single(model_name, order):
    sess = rt.InferenceSession(f"ml_models/{model_name}.onnx")

    data = {'produit_recu':[order.produit_recu],
            'temps_livraison':[order.temps_livraison]}
    df_to_predict = pd.DataFrame(data)

    input_name = sess.get_inputs()[0].name
    label_name = sess.get_outputs()[0].name

    prediction = sess.run([label_name], {input_name: df_to_predict.values.astype('float32')})[0]

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

# def get_model_name():
#     # Liste tous les fichiers dans le répertoire 'ml_models'
#     files = os.listdir('ml_models')
#     # Filtrer les fichiers .onnx
#     onnx_files = [f for f in files if f.endswith('.onnx')]
#     if onnx_files:
#         # Prendre le premier fichier .onnx, supprimer l'extension .onnx pour obtenir le nom du modèle
#         model_name = onnx_files[0][:-5]
#         return model_name
#     else:
#         return None

def get_db(db_name = "../olist.db"):
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

    recall_test = round(recall_score(y_test, model.predict(X_test)),4)
    acc_test = round(accuracy_score(y_test, model.predict(X_test)),4)
    f1_test = round(f1_score(y_test, model.predict(X_test)),4)

    try:
        # Convert the model to ONNX
        initial_type = [('float_input', FloatTensorType([None, 2]))]
        onnx_model = convert_sklearn(model, initial_types=initial_type)

        # Save the model
        with open(f"ml_models/{model_name}.onnx", "wb") as f:
            f.write(onnx_model.SerializeToString())
    except Exception as e:
        print(f"Erreur lors de la conversion ou de la sauvegarde du modèle : {e}")

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



