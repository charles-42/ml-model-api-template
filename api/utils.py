from fastapi import HTTPException, status, Depends
from jose import JWTError, jwt
import os
from pydantic import BaseModel
import pickle
import pandas as pd
import mlflow
from dotenv import load_dotenv
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


async def has_access(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    """ Check if the user has access to the endpoint. """
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


def predict_single(loaded_model, order):

    data = {'produit_recu': [order.produit_recu],
            'temps_livraison': [order.temps_livraison]}
    df_to_predict = pd.DataFrame(data)

    prediction = loaded_model.predict(df_to_predict)

    return prediction[0]


def get_model(run_name):
    with open(f"api/{run_name}.pkl", 'rb') as file:
        loaded_model = pickle.load(file)
    return loaded_model


def generate_token(to_encode):
    load_dotenv()
    SECRET_KEY = os.environ.get("SECRET_KEY")
    ALGORITHM = "HS256"
    to_encode_dict = {"sub": to_encode}
    encoded_jwt = jwt.encode(to_encode_dict, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


if __name__ == "__main__":
    print(generate_token("admin"))
