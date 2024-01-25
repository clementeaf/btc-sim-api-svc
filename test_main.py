from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_market_spread():
    response = client.get("/markets")
    assert response.status_code == 200
    assert "error" not in response.json()
