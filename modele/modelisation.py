def modelisation(connection,run_name):
    import pandas as pd
    import sqlite3
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import recall_score, accuracy_score, f1_score
    import pickle
    import mlflow

    mlflow.start_run(run_name=run_name)
    df = pd.read_sql_query(f"SELECT * FROM {run_name}_TrainingDataset",connection)
    df = df.dropna()

    y = df['score']
    X = df[["produit_recu","temps_livraison"]]
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, random_state=42)

    model = LogisticRegression()

    model.fit(X_train,y_train)


    recall_train = round(recall_score(y_train, model.predict(X_train)),4)
    acc_train = round(accuracy_score(y_train, model.predict(X_train)),4)
    f1_train = round(f1_score(y_train, model.predict(X_train)),4)

    mlflow.log_metric("recall_train", recall_train)
    mlflow.log_metric("accuracy_train", acc_train)
    mlflow.log_metric("f1_train", f1_train)

    print(f"Pour le jeu d'entrainement: \n le recall est de {recall_train}, \n l'accuracy de {acc_train} \n le f1 score de {f1_train}")

    recall_test = round(recall_score(y_test, model.predict(X_test)),4)
    acc_test = round(accuracy_score(y_test, model.predict(X_test)),4)
    f1_test = round(f1_score(y_test, model.predict(X_test)),4)

    mlflow.log_metric("recall_test", recall_test)
    mlflow.log_metric("accuracy_test", acc_test)
    mlflow.log_metric("f1_test", f1_test)
    
    # Save the model to MLflow
    mlflow.sklearn.log_model(model, "logistic_regression_model")

    # End MLflow run
    mlflow.end_run()
    

if __name__== "main":
    import sqlite3
    connection = sqlite3.connect("olist.db")