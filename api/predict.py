# main.py script
from fastapi import Depends
from api.utils import has_access
from fastapi import APIRouter
from fastapi.params import Depends
from api.utils import has_access, SinglePredictionInput, SinglePredictionOutput, predict_single, get_model_path
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

    model_name = "first_run_2017"
    model_path = get_model_path(model_name)
    prediction = predict_single(model_path, order)

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


