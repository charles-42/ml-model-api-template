from fastapi import APIRouter, HTTPException, Request
from fastapi.params import Depends
from sqlalchemy.orm import Session
from typing import List
from typing import List, Annotated
from api.database.core import NotFoundError, get_db
from api.database.authentificate import oauth2_scheme, has_access, User
from api.database.prediction import ModelTraining, ModelTrained, SinglePredictionOutput, BatchPredictionOutput, SinglePredictionInput, BatchPredictionInput, create_db_model, read_db_models
from api.utils import train, update_model_name, get_model_name

PROTECTED = Annotated[User, Depends(has_access)]



router = APIRouter(
    prefix="/prediction",
)

@router.post("/train")
def train_model(has_access: PROTECTED, request: Request, model: ModelTraining,db: Session = Depends(get_db)) -> ModelTrained:
    metrics = train(model.model_name)
    model_trained =  ModelTrained(**metrics)
    create_db_model(model_trained, db)
    return model_trained

@router.get("/models")
def get_models(request: Request, db: Session = Depends(get_db)) -> List[ModelTrained]:
    models = read_db_models(db)
    return models

@router.put("/update")
# def update_model(has_access: PROTECTED, request: Request, model_name: str):
def update_model(request: Request, model_name: str):
    update_model_name(model_name)
    return {"message": "model name updated"}


@router.post("/single", response_model=SinglePredictionOutput)
def predict_single(request: Request, order: SinglePredictionInput) -> SinglePredictionOutput:
    model_name = get_model_name()
    prediction = predict_single(model_name, order)
    return SinglePredictionOutput(prediction=prediction)

@router.post("/batch", response_model=List[SinglePredictionOutput])
def predict_batch(request: Request, orders:List[SinglePredictionInput], db: Session = Depends(get_db)) -> List[SinglePredictionOutput]:
    model_name = get_model_name()
    predictions = [predict_single(model_name, order) for order in orders]
    return [SinglePredictionOutput(prediction=prediction) for prediction in predictions]

