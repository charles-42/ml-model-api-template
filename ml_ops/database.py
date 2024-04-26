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