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
    """
    Validates the access token provided in the request headers.

    Args:
        credentials (HTTPAuthorizationCredentials): The bearer token credentials.

    Returns:
        bool: True if the user has access, otherwise raises HTTPException.

    Raises:
        HTTPException: If the token is invalid or the user is not authorized.
    """
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
    """
    Model for single prediction input.

    Attributes:
        produit_recu (int): The quantity of the received product.
        temps_livraison (int): The delivery time.
    """
    produit_recu: int
    temps_livraison: int


class SinglePredictionOutput(BaseModel):
    """
    Model for single prediction output.

    Attributes:
        prediction (int): The predicted value.
    """
    prediction: int


def predict_single(loaded_model, order):
    """
    Make a prediction using the loaded model and the input order.

    Args:
        loaded_model: The pre-trained model.
        order (SinglePredictionInput): The input data for making the prediction.

    Returns:
        int: The predicted value.
    """
    data = {'produit_recu': [order.produit_recu],
            'temps_livraison': [order.temps_livraison]}
    df_to_predict = pd.DataFrame(data)

    prediction = loaded_model.predict(df_to_predict)

    return prediction[0]


def get_model(run_name):
    """
    Load a model from a pickle file.

    Args:
        run_name (str): The name of the model run.

    Returns:
        The loaded model.
    """
    with open(f"api/{run_name}.pkl", 'rb') as file:
        loaded_model = pickle.load(file)
    return loaded_model


def generate_token(to_encode):
    """
    Generate a JWT token.

    Args:
        to_encode (str): The string to encode in the token.

    Returns:
        str: The generated JWT token.
    """
    load_dotenv()
    SECRET_KEY = os.environ.get("SECRET_KEY")
    ALGORITHM = "HS256"
    to_encode_dict = {"sub": to_encode}
    encoded_jwt = jwt.encode(to_encode_dict, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


if __name__ == "__main__":
    print(generate_token("admin"))
