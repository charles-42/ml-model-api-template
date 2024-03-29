FROM python:3.10.14


WORKDIR /app


COPY setup.sh .
COPY requirements.txt .

RUN apt-get update && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get install -y sqlite3

RUN chmod +x ./setup.sh

RUN ./setup.sh

COPY . .

CMD [ "python3", "api/main.py" ]