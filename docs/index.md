# data-api-template

## Purpose

The objective of this project is to provide a standard template for creating a data API. 


It includes:

- The procedure for building a Postgres SQL database on Azure and procedure for importing data.
- A machine learning model including pytest quality tests and mlflow tracking on azure
- An API (FastAPI) with token-based authentication and Ml-ops Monitoring
- A Streamlit dashboard to expose Ml-ops Monitoring

## Dependencies:
- poetry
- azure CLI
- azure ml CLI
- psql

## Setup

1. Create virtual environement and install requierements:

```bash

poetry install

```

2. Create .env file using env_template.txt


3. To create the Olist database, execute these commands:

```bash
chmod +x ./database/azure_postgres/create_postgres.sh
./database/azure_postgres/create_postgres.sh

chmod +x ./database/azure_postgres/create_tables.sh
./database/azure_postgres/create_tables.sh

chmod +x ./database/azure_postgres/import_postgres.sh
./database/azure_postgres/import_postgres.sh
```

4. You can execute tests to make sure the setup is good:

```bash
pytest
```
## Train a new model

You can update training functions and then use ./model/train.sh to train a new model. (Don't forget to change run_name)

## Launch the API

1. Get your token:

```bash
poetry run python -m api.utils
```

2. Update model_name in ./api/launch_app.sh and then you can execute it

## Use Streamlit ML-OPS Dashboard

Execute this command

```bash
poetry run streamlit run ml_ops/dashboard.py
```