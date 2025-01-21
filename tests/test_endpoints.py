from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Test for the /api/v1/delivery-order-price endpoint
def test_delivery_order_price():
    params = {
        "venue_slug": "home-assignment-venue-helsinki",
        "cart_value": 1000,
        "user_lat": 60.17094,
        "user_lon": 24.93087
    }

    # Sending POST request to the endpoint
    response = client.get("/api/v1/delivery-order-price", params=params)

    # Asserting the response status code and content
    assert response.status_code == 200

def test_delivery_order_price_bad_request():
    params = {
        "venue_slug": "home-assignment-venue-helsinki",
        "cart_value": 1000,
        "user_lat": 600.17094,
        "user_lon": 240.93087
    }

    # Sending POST request to the endpoint
    response = client.get("/api/v1/delivery-order-price", params=params)

    # Asserting the response status code and content
    assert response.status_code == 400
    assert response.json() == {'detail':'Delivery not possible for distances beyond 2000 meters.'}
