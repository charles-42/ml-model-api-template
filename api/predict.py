# main.py script
from fastapi import Depends
from api.utils import has_access
from fastapi import APIRouter
from fastapi.params import Depends
from api.utils import has_access, SinglePredictionInput, SinglePredictionOutput, predict_single, get_model_path




router = APIRouter()

@router.post("", response_model=SinglePredictionOutput)
def predict(order: SinglePredictionInput, authenticated: bool = [Depends(has_access)]) -> SinglePredictionOutput:
    model_path = get_model_path("first_run_2017")
    prediction = predict_single(model_path, order)
    return SinglePredictionOutput(prediction=prediction)