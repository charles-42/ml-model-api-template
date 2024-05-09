FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

WORKDIR /app

RUN mkdir /app/api

COPY ./requirements.txt /app/api/requirements.txt

RUN python -m pip install --no-cache-dir --upgrade  -r /app/api/requirements.txt

COPY . /app/api

# ENV PATH ${APP_ROOT}/.local/bin:${PATH}

CMD ["/app/api/launch_app.sh"]