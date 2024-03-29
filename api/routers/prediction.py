from fastapi import APIRouter, HTTPException, Request
from fastapi.params import Depends
from sqlalchemy.orm import Session
from typing import List
from typing import List, Annotated
from database.core import NotFoundError, get_db
from database.authentificate import oauth2_scheme, has_access, User
from database.prediction import ModelTraining, ModelTrained, SinglePredictionOutput, BatchPredictionOutput, SinglePredictionInput, BatchPredictionInput, create_db_model, read_db_models
from utils import train, update_model_name, get_model_name, prediction_single

import logging

PROTECTED = Annotated[User, Depends(has_access)]

router = APIRouter(
    prefix="/prediction",
)


logger = logging.getLogger("api_model.prediction")

@router.post("/train")
def train_model(has_access: PROTECTED, request: Request, model: ModelTraining, db: Session = Depends(get_db)) -> ModelTrained:
    logger.debug(f"Starting model training: {model.model_name}")
    try:
        metrics = train(model.model_name)
        model_trained = ModelTrained(**metrics)
        create_db_model(model_trained, db)
        logger.info(f"Model {model.model_name} trained successfully")
        return model_trained
    except Exception as e:
        logger.error(f"Model training failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Model training failed")

@router.get("/models")
def get_models(request: Request, db: Session = Depends(get_db)) -> List[ModelTrained]:
    logger.debug("Fetching all models")
    models = read_db_models(db)
    logger.info(f"Fetched {len(models)} models")
    return models

@router.put("/update")
def update_model(has_access: PROTECTED, request: Request, model_name: str):
    logger.debug(f"Updating model: {model_name}")
    try:
        update_model_name(model_name)
        logger.info(f"Model updated: {model_name}")
        return {"message": "Model name updated"}
    except Exception as e:
        logger.error(f"Failed to update model: {e}", exc_info=True)
        return {"message": "Failed to update model name"}

@router.post("/single")
def predict_single(request: Request, order: SinglePredictionInput) -> SinglePredictionOutput:
    logger.debug("Making single prediction")
    prediction = prediction_single(get_model_name(), order)
    logger.info("Single prediction made")
    return SinglePredictionOutput(prediction=prediction)

@router.post("/batch")
def predict_batch(request: Request, orders: List[SinglePredictionInput], db: Session = Depends(get_db)) -> List[SinglePredictionOutput]:
    logger.debug(f"Making batch predictions for {len(orders)} orders")
    predictions = [prediction_single(get_model_name(), order) for order in orders]
    logger.info("Batch predictions made")
    return [SinglePredictionOutput(prediction=prediction) for prediction in predictions]



# @router.post("/train")
# def train_model(has_access: PROTECTED, request: Request, model: ModelTraining,db: Session = Depends(get_db)) -> ModelTrained:
#     metrics = train(model.model_name)
#     model_trained =  ModelTrained(**metrics)
#     create_db_model(model_trained, db)
#     return model_trained

# @router.get("/models")
# def get_models(request: Request, db: Session = Depends(get_db)) -> List[ModelTrained]:
#     models = read_db_models(db)
#     return models

# @router.put("/update")
# # def update_model(has_access: PROTECTED, request: Request, model_name: str):
# def update_model(request: Request, model_name: str):
#     update_model_name(model_name)
#     return {"message": "model name updated"}


# @router.post("/single", response_model=SinglePredictionOutput)
# def predict_single(request: Request, order: SinglePredictionInput) -> SinglePredictionOutput:
#     model_name = get_model_name()
#     prediction = prediction_single(model_name, order)
#     return SinglePredictionOutput(prediction=prediction)

# @router.post("/batch", response_model=List[SinglePredictionOutput])
# def predict_batch(request: Request, orders:List[SinglePredictionInput], db: Session = Depends(get_db)) -> List[SinglePredictionOutput]:
#     model_name = get_model_name()
#     predictions = [prediction_single(model_name, order) for order in orders]
#     return [SinglePredictionOutput(prediction=prediction) for prediction in predictions]