# main.py script
from fastapi import FastAPI, Depends
import api.predict
from api.utils import has_access
from fastapi import FastAPI
from fastapi.params import Depends
from api.utils import has_access


app = FastAPI()

# routes
PROTECTED = [Depends(has_access)]

app.include_router(
    api.predict.router,
    prefix="/predict",
    dependencies=PROTECTED
)
