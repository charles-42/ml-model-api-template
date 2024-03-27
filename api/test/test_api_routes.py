from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker, Session
from api.database.core import Base, get_db, DBModel
from api.database.authentificate import create_db_user, UserCreate
from api.database.prediction import ModelTraining
from api.main import app
from typing import Generator
import pytest 
from unittest.mock import MagicMock
from api.utils import train

TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread":False},poolclass=StaticPool)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def session() -> Generator[Session, None, None]:
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

    #create test user
    create_db_user( 
        UserCreate( 
            username="test_user",
            email = "test_user@test.com",
            full_name="test_user_fullname",
            password = "test_password"
            ), 
            db_session)
    
    yield db_session

    db_session.close()
    Base.metadata.drop_all(bind=engine)



# Define a pytest fixture to mock the dependencies
@pytest.fixture(autouse=False)
def valid_token(monkeypatch):
    # Mock the jwt.decode function to return the mock payload
    monkeypatch.setattr("jose.jwt.decode", MagicMock(return_value={"sub": "test_user"}))


# Define a pytest fixture to mock the dependencies
@pytest.fixture(autouse=False)
def mock_train(monkeypatch):
    # Mock the jwt.decode function to return the mock payload
    monkeypatch.setattr("api.routers.prediction.train", MagicMock(return_value={
        "model_name": "test_model_3",
        "recall_train": 0.5,
        "acc_train": 0.5,
        "f1_train": 0.5,
        "recall_test": 0.5,
        "acc_test": 0.5,
        "f1_test": 0.5
    }
))

@pytest.fixture(autouse=False)
def mock_get_model_name(monkeypatch):
    # Mock the jwt.decode function to return the mock payload
    monkeypatch.setattr("api.routers.prediction.get_model_name", MagicMock(return_value="test_model"))

@pytest.fixture(autouse=False)
def mock_predict_single(monkeypatch):
    # Mock the jwt.decode function to return the mock payload
    monkeypatch.setattr("api.routers.prediction.predict_single", MagicMock(return_value=1))



client  = TestClient(app)


# Dependency to override the get_db dependency in the main app
def override_get_db():
    database = TestingSessionLocal()
    yield database
    database.close()

# # using dependency overrides to mock the functions
# app.dependency_overrides[train] = mock_train

app.dependency_overrides[get_db] = override_get_db

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == 'Server is running.'

def test_train_unauthorize(session:Session):
    response = client.post("prediction/train/",json={
            "model_name":"test_2"})
    assert response.status_code == 401, response.text


def test_create_improper_train(session:Session, valid_token):
    response = client.post("prediction/train/",json={
            "wrong_argument":"test_2"}, headers={"Authorization": f"Bearer {'mocked_token'}"})
    assert response.status_code == 422, response.text

def test_train_model(session:Session, valid_token, mock_train):
    response = client.post("prediction/train/",json={
            "model_name":"test_2"}, headers={"Authorization": f"Bearer {'mocked_token'}"})
    assert response.status_code == 200, response.text
    assert 'model_name' in response.json()

def test_predict_single(mock_get_model_name,mock_predict_single):
    # Assuming SinglePredictionInput is a pydantic model
    data = {"produit_recu":1, "temps_livraison":12}
          # Replace with actual input data
    response = client.post("prediction/single/", json=data)
    assert response.status_code == 200
    # Assuming predict_single returns a valid prediction
    assert "prediction" in response.json()

def test_predict_batch(mock_get_model_name,mock_predict_single):
    # Assuming SinglePredictionInput is a pydantic model
    data = [{"produit_recu":1, "temps_livraison":12},{"produit_recu":0, "temps_livraison":12}]
          # Replace with actual input data
    response = client.post("prediction/batch/", json=data)
    assert response.status_code == 200
    # Assuming predict_single returns a valid prediction
    assert len(response.json()) == 2



####  Authentification

def test_create_user(session:Session):
    response = client.post("/auth/create_user",json={
            "username":"test_user_2",
            "email" : "test_user@test.com",
            "full_name":"test_user_fullname",
            "password" : "test_password"
            })
    assert response.status_code == 200, response.text
    assert 'username' in response.json() 


def test_login_for_access_token(session):


    # Make a request to the endpoint
    response = client.post(
        "/auth/token",
        data={"username": "test_user", "password": "test_password"}
    )

    # Assert the response status code
    assert response.status_code == 200

    # Assert that the response contains the access token
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"



