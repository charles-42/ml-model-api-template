from fastapi import FastAPI, APIRouter
from routers.prediction import router as prediction_router, train
from routers.authentificate import router as authentificate_router

test_router = APIRouter()

app = FastAPI()

app.include_router(prediction_router)

app.include_router(authentificate_router)

@app.get("/")
def read_root():
    return "Server is running."

