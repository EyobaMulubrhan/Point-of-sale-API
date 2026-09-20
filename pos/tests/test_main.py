from fastapi.testclient import TestClient
from pos.main import app

client =TestClient(app)


def test_home():
    response = client.get("/")
    print(response.json())
    assert response.status_code == 200