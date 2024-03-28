from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column


DATABASE_URL = "sqlite:///olist.db"

class NotFoundError(Exception):
    pass


class Base(DeclarativeBase):
    pass

class DBUsers(Base):

    __tablename__ = "users"

    username: Mapped[str] = mapped_column(primary_key=True, index=True)
    email: Mapped[str]
    full_name: Mapped[str]
    disabled: Mapped[bool] = mapped_column(default=False)
    hashed_password: Mapped[str]

class DBToken(Base):

    __tablename__ = "tokens"

    username: Mapped[str] = mapped_column(primary_key=True, index=True)



class DBModel(Base):
      
    __tablename__ = "models"

    model_name: Mapped[str] = mapped_column(primary_key=True, index=True)
    recall_train : Mapped[float]
    acc_train: Mapped[float]
    f1_train: Mapped[float]
    recall_test: Mapped[float]
    acc_test: Mapped[float]
    f1_test: Mapped[float]
    
################################################################################   
class DBToPredict(Base):
          
    __tablename__ = "topredict"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    produit_recu: Mapped[int] 
    temps_livraison: Mapped[int] 
    
class DBPrediction(Base):
          
    __tablename__ = "prediction"
    
    id : Mapped[int] = mapped_column(primary_key=True, index=True)
    prediction : Mapped[int]
    
################################################################################

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
