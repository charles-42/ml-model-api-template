from fastapi import FastAPI, APIRouter, Request
from api.routers.prediction import router as prediction_router, train
from routers.authentificate import router as authentificate_router
from api.logs.config import setup_logging_config

import time
import logging

test_router = APIRouter()

app = FastAPI()
setup_logging_config()

app.include_router(prediction_router)

app.include_router(authentificate_router)

@app.get("/")
def read_root():
    return "Server is running."


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger = logging.getLogger("api_model.requests")
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    logger.info(f"Request {request.method} {request.url.path} completed in {duration:.2f}s with status {response.status_code}")
    return response


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)