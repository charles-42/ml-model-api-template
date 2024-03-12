from typing import List
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .core import NotFoundError, DBModel
import string
import random
import json

class ModelTraining(BaseModel):
    model_name:str

class ModelTrained(BaseModel):
    model_name:str
    recall_train:float
    acc_train:float
    f1_train:float
    recall_test:float
    acc_test:float
    f1_test:float



class BatchPredictionInput(BaseModel):
    pass

class BatchPredictionOutput(BaseModel):
    pass

class SinglePredictionInput(BaseModel):
    produit_recu: int
    temps_livraison: int

class SinglePredictionOutput(BaseModel):
    prediction: int


def create_db_model(model_trained: ModelTrained, session: Session) -> None:
    db_model = DBModel(**model_trained.model_dump(exclude_none=True))
    session.add(db_model)
    session.commit()
    session.refresh(db_model)

def read_db_models(session: Session) -> List[DBModel]:
    db_model = session.query(DBModel).all()
    if db_model is None:
        raise NotFoundError(f"Database is empty")
    return db_model