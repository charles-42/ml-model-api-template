from typing import List
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .core import NotFoundError, DBModel, DBToPredict, DBPrediction
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
    
class PredictionImput(BaseModel):
    id : int
    prediction: int
    
class ValidateId(BaseModel):
    entry_id : int 
    
#############################################################################

class CreateDB():
    
    def __init__(self, session: Session):
        self.session = session
        
    def create_db_model(self, model_trained: ModelTrained) -> None:
        db_model = DBModel(**model_trained.model_dump(exclude_none=True))
        self.session.add(db_model)
        self.session.commit()
        self.session.refresh(db_model)
        

    def read_db_models(self) -> List[DBModel]:
        db_models = self.session.query(DBModel).all()
        if not db_models:
            raise NotFoundError("Database is empty")
        return db_models

        
    def ceate_db_to_predict(self, topredict : SinglePredictionInput) -> None:
        new_entry = DBToPredict(**topredict.dict())
        self.session.add(new_entry)
        self.session.commit()
        self.session.refresh(new_entry)
        
    
    def read_db_to_predict(self) -> List[DBToPredict]:
        entries = self.session.query(DBToPredict).all()
        if not entries:
            raise NotFoundError("Database is empty")
        return entries
        
    
    def ceate_db_prediction(self, prediction : PredictionImput) -> None:
        new_entry = DBPrediction(**prediction.dict())
        self.session.add(new_entry)
        self.session.commit()
        self.session.refresh(new_entry)
        
    
    def read_db_prediction(self) -> List[DBPrediction]:
        entries = self.session.query(DBPrediction).all()
        if not entries:
            raise NotFoundError("Database is empty")
        return entries
        
        
    def to_predict(self, topredict : SinglePredictionInput) -> ValidateId:
        new_entry = DBToPredict(**topredict.dict())
        self.session.add(new_entry)
        self.session.commit()
        self.session.refresh(new_entry)
        return new_entry.id
    
    def get_prediction_by_id(self, entry_id: ValidateId) -> SinglePredictionOutput:
        prediction_entry = self.session.query(DBPrediction).filter_by(id=entry_id).first()
        if not prediction_entry:
            raise NotFoundError("Database is empty")
        return prediction_entry.prediction
    
###########################################################################