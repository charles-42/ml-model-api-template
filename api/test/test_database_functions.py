from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker, Session
from database.core import Base, DBModel
from typing import Generator
from database.prediction import create_db_model,read_db_models, ModelTrained
import pytest

@pytest.fixture
def session() -> Generator[Session, None, None]:
    TEST_DATABASE_URL = "sqlite:///:memory:"

    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread":False},poolclass=StaticPool)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base.metadata.create_all(bind=engine)
    db_session = TestingSessionLocal()

    #create test models
    db_model = DBModel(
            model_name = "test_model",
            recall_train = 0.5,
            acc_train = 0.5,
            f1_train = 0.5,
            recall_test = 0.5,
            acc_test = 0.5,
            f1_test = 0.5)
    db_session.add(db_model)
    db_session.commit()

    yield db_session

    db_session.close()
    Base.metadata.drop_all(bind=engine)


def test_create_model(session:Session) -> None: 
    create_db_model(
        ModelTrained(
            model_name = "test_model_2",
            recall_train = 0.5,
            acc_train = 0.5,
            f1_train = 0.5,
            recall_test = 0.5,
            acc_test = 0.5,
            f1_test = 0.5 
            ),

            session)
    
    model =  session.query(DBModel).filter(DBModel.model_name == "test_model_2").first()
    assert model.model_name == "test_model_2"
    assert model.recall_train == 0.5
    assert model.acc_train == 0.5
    assert model.f1_train == 0.5
    assert model.recall_test == 0.5
    assert model.acc_test == 0.5

def test_read_models(session:Session) -> None:
    models = read_db_models(session)
    assert len(models) == 1
    assert models[0].model_name == "test_model"
    assert models[0].recall_train == 0.5
    assert models[0].acc_train == 0.5
    assert models[0].f1_train == 0.5
    assert models[0].recall_test == 0.5
    assert models[0].acc_test == 0.5
    assert models[0].f1_test == 0.5
    