from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

def connect_to_postgres():
    load_dotenv()
    # Define your PostgreSQL connection parameters
    hostname = os.environ.get("SERVER")
    database = os.environ.get("DATABASE")
    username = os.environ.get("POSTGRES_USER")
    password = os.environ.get("PASSWORD")

    # Create a connection to the PostgreSQL database
    connection_string = f"postgresql://{username}:{password}@{hostname}/{database}"

    engine = create_engine(connection_string)

    return engine

def get_run(run_name,experiment_name):
    from azureml.core import Workspace
    from azureml.core import Experiment
    from dotenv import load_dotenv
    import os

    load_dotenv()

    # Provide your workspace details
    subscription_id = os.getenv("SUBSCRIPTION_ID")
    resource_group = os.getenv("RESSOURCE_GROUP")
    workspace_name = os.getenv("WORKSPACE_NAME")


    ws = Workspace(subscription_id=subscription_id,
                    resource_group=resource_group,
                    workspace_name=workspace_name)


    experiment = Experiment(ws, experiment_name)
    # runs = [run for run in experiment.get_runs()]
    run = next(run for run in experiment.get_runs() if run.tags['mlflow.runName']==run_name)
    return run