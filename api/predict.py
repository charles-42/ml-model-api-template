# main.py script
from fastapi import Depends
from fastapi import APIRouter
from fastapi.params import Depends
from api.utils import has_access, SinglePredictionInput, SinglePredictionOutput, predict_single, get_model
from api.database import get_db,create_db_prediction
from sqlalchemy.orm import Session
import time


router = APIRouter()

@router.post("", response_model=SinglePredictionOutput)
def predict(
    order: SinglePredictionInput, 
    authenticated: bool = [Depends(has_access)],
    db: Session = Depends(get_db)
    ) -> SinglePredictionOutput:

    model_name = "remote_run"
    model = get_model(model_name)
    prediction = predict_single(model, order)

    # MLops: Save prediction to database
    prediction_dict = {
        "prediction": int(prediction),
        "produit_recu": order.produit_recu,
        "temps_livraison": order.temps_livraison,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "model":model_name
    }
    create_db_prediction(prediction_dict, db)

    return SinglePredictionOutput(prediction=prediction)


