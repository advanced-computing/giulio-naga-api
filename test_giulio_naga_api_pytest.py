import pytest
from giulio_naga_api import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_homepage(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"<table" in response.data

def test_pagination(client):
    response = client.get("/?offset=10&limit=5")
    assert response.status_code == 200 
    assert b"<table" in response.data

def test_intern_endpoint(client):
    response = client.get("/intern")
    assert response.status_code == 200
    assert isinstance(response.json, dict)
