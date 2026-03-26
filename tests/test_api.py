# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Basic API test
def test_create_address():
    response = client.post("/api/v1/addresses", json={      #posting json dta to test through clint
        "name": "Test Location",
        "latitude": 28.61,
        "longitude": 77.20
    })
#showing http status codes after success of post method
    assert response.status_code == 200      