from fastapi import APIRouter, HTTPException, Request
from fastapi.params import Depends
from sqlalchemy.orm import Session
from typing import List
from typing import List, Annotated
from database.core import NotFoundError, get_db
from database.authentificate import oauth2_scheme, has_access, User
from database.prediction import ModelTraining, ModelTrained, SinglePredictionOutput,  SinglePredictionInput, CreateDB, ValidateId, PredictionImput
from utils import train, update_model_name, get_model_name, make_predictions

PROTECTED = Annotated[User, Depends(has_access)]



router = APIRouter(
    prefix="/prediction",
)

@router.post("/train")
def train_model(has_access: PROTECTED, request: Request, model: ModelTraining,db: Session = Depends(get_db)) -> ModelTrained:
    metrics = train(model.model_name)
    model_trained =  ModelTrained(**metrics)
    db_manager = CreateDB(session=db)
    db_manager.create_db_model(model_trained)
    return model_trained

@router.get("/models")
def get_models(request: Request, db: Session = Depends(get_db)) -> List[ModelTrained]:
    db_manager = CreateDB(session=db)
    models = db_manager.read_db_models()
    return models

@router.put("/update")
# def update_model(has_access: PROTECTED, request: Request, model_name: str):
def update_model(request: Request, model_name: str):
    update_model_name(model_name)
    return {"message": "model name updated"}

#################################################################################################

@router.post("/to_predict")
def to_predict(request: Request, order: SinglePredictionInput, db: Session = Depends(get_db)):
    db_manager = CreateDB(session=db)
    new_entry_id = db_manager.to_predict(order)
    return {"votre id est": new_entry_id}


@router.get("/prediction")
def get_prediction(request: Request, entry_id: int, db: Session = Depends(get_db)):
    db_manager = CreateDB(session=db)
    prediction_entry = db_manager.get_prediction_by_id(entry_id)
    return {f"La prediction pour l'id {entry_id} est {prediction_entry}"}


@router.post("/to_schedule")
def make_migration(request: Request, db: Session = Depends(get_db)):
    make_predictions(db)
    return {"Les mission est faite avec succés"}
   
    

# #test pour inserer des données dans la table prediction 
# @router.post("/post_data")
# def test(request: Request, order: PredictionImput, db: Session = Depends(get_db)):
#     db_manager = CreateDB(session=db)
#     db_manager.ceate_db_prediction(order)

# #test pour affciher ce qu on a ajouté dans la table prediction
# @router.get("/get_all_prediction")
# def get_all(request: Request , db: Session = Depends(get_db)) -> List[PredictionImput]:
#     db_manager = CreateDB(session=db)
#     return [raw for raw in db_manager.read_db_prediction()]
    
###################################################################################
    


    
    
    