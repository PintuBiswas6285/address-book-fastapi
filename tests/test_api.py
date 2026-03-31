from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Basic API test
def test_create_address():
    response = client.post("/api/v1/addresses", json={
        "name": "Test Location",
        "latitude": 28.61,
        "longitude": 77.20
    })

    assert response.status_code == 200