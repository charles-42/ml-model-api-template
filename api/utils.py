from fastapi import  HTTPException, status, Depends
from jose import JWTError, jwt
import os
from pydantic import BaseModel
import pickle
import pandas as pd
import mlflow
from dotenv import load_dotenv
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


async def has_access(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    token = credentials.credentials
    load_dotenv()
    SECRET_KEY = os.environ.get("SECRET_KEY")
    ALGORITHM = "HS256"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
    except JWTError:
        raise credentials_exception
    if username == "admin":
        return True
    else:
        raise credentials_exception


class SinglePredictionInput(BaseModel):
    produit_recu: int
    temps_livraison: int

class SinglePredictionOutput(BaseModel):
    prediction: int

def predict_single(model_path, order):

    with open(model_path, 'rb') as file:
        loaded_model = pickle.load(file)

    data = {'produit_recu':[order.produit_recu],
            'temps_livraison':[order.temps_livraison]}
    df_to_predict = pd.DataFrame(data)

    prediction = loaded_model.predict(df_to_predict)

    return prediction[0]

def get_model_path(model_run):
    experiment = mlflow.get_experiment_by_name("predict_review_score")
    runs = mlflow.search_runs(experiment_ids=experiment.experiment_id)
    filtered_runs = runs[runs['tags.mlflow.runName'] == model_run]
    run_id = filtered_runs.iloc[0]['run_id']
    run = mlflow.get_run(run_id)
    artifact_uri = run.info.artifact_uri
    model_path = os.path.join(artifact_uri.replace("file://", ""), model_run, "model.pkl")
    return model_path

def generate_token(to_encode):
    load_dotenv()
    SECRET_KEY = os.environ.get("SECRET_KEY")
    ALGORITHM = "HS256"
    to_encode_dict = {"sub": to_encode}
    encoded_jwt = jwt.encode(to_encode_dict, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



if __name__ == "__main__":
    print(generate_token("admin"))