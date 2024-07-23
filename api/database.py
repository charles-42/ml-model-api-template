from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column
from sqlalchemy.orm import Session
import string
import random

from sqlalchemy import create_engine
from dotenv import load_dotenv
import os


def connect_to_postgres(): 
    """
    Connect to a PostgreSQL database using environment variables.

    Returns:
        engine: SQLAlchemy engine instance for the PostgreSQL connection.
    """
    load_dotenv()
    # Define your PostgreSQL connection parameters
    hostname = os.environ.get("SERVER")
    database = os.environ.get("DATABASE")
    username = os.environ.get("POSTGRES_USER")
    password = os.environ.get("PASSWORD")

    # Create a connection to the PostgreSQL database
    connection_string = f"postgresql://{username}:{password}@{hostname}/{database}"
    print(connection_string)
    engine = create_engine(connection_string)
    print(engine)
    return engine


class Base(DeclarativeBase):
    """Base class for SQLAlchemy ORM models."""
    pass


class DBpredictions(Base):
    """
    ORM model for the 'predictions' table.

    Attributes:
        prediction_id (str): Primary key, unique identifier for the prediction.
        timestamp (str): Timestamp of the prediction.
        produit_recu (int): Quantity of the received product.
        temps_livraison (int): Delivery time.
        prediction (int): The prediction value.
        model (str): The model used for the prediction.
    """
    __tablename__ = "predictions"

    prediction_id: Mapped[str] = mapped_column(primary_key=True, index=True)
    timestamp: Mapped[str]
    produit_recu: Mapped[int]
    temps_livraison: Mapped[int]
    prediction: Mapped[int]
    model: Mapped[str]


def get_db():
    """
    Dependency to get the database session.

    Yields:
        Session: SQLAlchemy database session.
    """
    engine = connect_to_postgres()
    session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    database = session_local()
    try:
        yield database
    finally:
        database.close()


def generate_id():
    """
    Generate a unique string ID.

    Returns:
        str: A randomly generated unique string ID.
    """
    length = 14
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))


def create_db_prediction(prediction: dict, session: Session) -> DBpredictions:
    """
    Create a new prediction record in the database.

    Args:
        prediction (dict): A dictionary containing prediction details.
        session (Session): SQLAlchemy session object.

    Returns:
        DBpredictions: The newly created DBpredictions object.
    """
    db_prediction = DBpredictions(**prediction, prediction_id=generate_id())
    session.add(db_prediction)
    session.commit()
    session.refresh(db_prediction)
    return db_prediction


if __name__ == '__main__':
    engine = connect_to_postgres()
    session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
