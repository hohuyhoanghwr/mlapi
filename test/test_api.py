from fastapi.testclient import TestClient
from app.main import app
import os

client = TestClient(app)
# Set up environment variable for testing
os.environ["API_TOKEN"] = os.getenv("API_TOKEN")


def test_full_input_prediction():
    headers = {"x-api-token": f"{os.environ['API_TOKEN']}"}
    response = client.post("/predict", json={
        "sepal_length": 2,
        "sepal_width": 2,
        "petal_length": 0.5,
        "petal_width": 3
    }, headers=headers)
    assert response.status_code == 200
    assert "predicted_species" in response.json()


def test_missing_one_field():
    headers = {"x-api-token": f"{os.environ['API_TOKEN']}"}
    response = client.post("/predict", json={
        "sepal_length": 1,
        "sepal_width": 4,
        "petal_width": 3
    }, headers=headers)
    assert response.status_code == 200
    assert "predicted_species" in response.json()


def test_missing_two_fields():
    headers = {"x-api-token": f"{os.environ['API_TOKEN']}"}
    response = client.post("/predict", json={
        "sepal_length": 1,
        "sepal_width": 4
    }, headers=headers)
    assert response.status_code == 200
    assert "predicted_species" in response.json()


def test_string_numbers_should_be_converted():
    headers = {"x-api-token": f"{os.environ['API_TOKEN']}"}
    response = client.post("/predict", json={
        "sepal_length": "4",
        "sepal_width": "3",
        "petal_length": 1,
        "petal_width": 2
    }, headers=headers)
    assert response.status_code == 200
    assert "predicted_species" in response.json()


def test_non_float_text_should_be_treated_as_missing():
    headers = {"x-api-token": f"{os.environ['API_TOKEN']}"}
    response = client.post("/predict", json={
        "sepal_length": "BIPM",
        "sepal_width": 3,
        "petal_length": "Hallo",
        "petal_width": 2
    }, headers=headers)
    assert response.status_code == 200
    assert "predicted_species" in response.json()

valid_payload = {
    "sepal_length": 5.1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2
}

def test_predict_success():
    response = client.post(
        "/predict",
        json=valid_payload,
        headers={"X-API-Token": f"{os.environ['API_TOKEN']}"}
    )
    assert response.status_code == 200
    assert "predicted_species" in response.json()

def test_predict_invalid_token():
    response = client.post(
        "/predict",
        json=valid_payload,
        headers={"X-API-Token": "Donald Trump"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Unauthorized"
