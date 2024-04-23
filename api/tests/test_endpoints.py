from fastapi.testclient import TestClient
from api.main import app
import pytest 
from unittest.mock import MagicMock

@pytest.fixture(autouse=False)
def valid_token(monkeypatch):
    # Mock the jwt.decode function to return the mock payload
    monkeypatch.setattr("jose.jwt.decode", MagicMock(return_value={"sub": "admin"}))

@pytest.fixture(autouse=False)
def mock_predict_single(monkeypatch):
    # Mock the jwt.decode function to return the mock payload
    monkeypatch.setattr("api.main.predict_single", MagicMock(return_value=1))



client  = TestClient(app)

def test_train_unauthorize():
    data = {"produit_recu":1, "temps_livraison":12}
    headers = {"Authorization": "Bearer false_token"}
    response = client.post("predict",json=data, headers=headers)
    assert response.status_code == 401, response.text

def test_predict_single(valid_token,mock_predict_single):
    # Assuming SinglePredictionInput is a pydantic model
    data = {"produit_recu":1, "temps_livraison":12}
          # Replace with actual input data
    headers = {"Authorization": "Bearer mock_token"}
    response = client.post("predict",json=data, headers=headers)
    assert response.status_code == 200
    # Assuming predict_single returns a valid prediction
    assert "prediction" in response.json()