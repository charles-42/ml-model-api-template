# main.py script
from fastapi import FastAPI, Depends
import api.opentelemetry_setup

import api.predict
from api.utils import has_access
from fastapi import FastAPI
from fastapi.params import Depends
from api.utils import has_access
import sys
import uvicorn
from api.opentelemetry_setup import init_tracing


app = FastAPI()

init_tracing(app)
# routes
PROTECTED = [Depends(has_access)]

app.include_router(
    api.predict.router,
    prefix="/predict",
    dependencies=PROTECTED
)

if __name__ == "__main__":
    args = sys.argv
    port = 8000
    if len(args) > 1:
        port_string = args[1]
        port = int(port_string)

    uvicorn.run(app, host="0.0.0.0", port=port)
