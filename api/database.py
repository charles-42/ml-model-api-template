from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column
from sqlalchemy.orm import Session
import string
import random

DATABASE_URL = "sqlite:///olist.db"

class Base(DeclarativeBase):
    pass


class DBpredictions(Base):

    __tablename__ = "predictions"

    prediction_id: Mapped[str] = mapped_column(primary_key=True, index=True)
    timestamp: Mapped[str]
    produit_recu: Mapped[int] 
    temps_livraison: Mapped[int]
    prediction: Mapped[int]
    model: Mapped[str]


engine = create_engine(DATABASE_URL)
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

# Dependency to get the database session
def get_db():
    database = session_local()
    try:
        yield database
    finally:
        database.close()

def generate_id():
    """Generate a unique string ID."""
    length = 14
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))


def create_db_prediction(prediction: dict, session: Session) -> DBpredictions:
    db_prediction = DBpredictions(**prediction, prediction_id=generate_id())
    session.add(db_prediction)
    session.commit()
    session.refresh(db_prediction)
    return db_prediction
