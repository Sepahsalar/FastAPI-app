from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_calculate_delivery_fee():
	payload = {
		"cart_value": 790,
		"delivery_distance": 2235,
		"number_of_items": 4,
		"time": "2024-01-15T13:00:00Z"}

	response = client.post("/calculate_delivery_fee", json=payload)
	assert response.status_code == 200
	assert "delivery_fee" in response.json()

def test_invalid_payload():
	# Test with invalid payload
	payload = {"invalid_key": "invalid_value"}
	
	response = client.post("/calculate_delivery_fee", json=payload)
	assert response.status_code == 422
	assert "detail" in response.json()
