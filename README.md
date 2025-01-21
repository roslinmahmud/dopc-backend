# Delivery Order Price Calculator (DOPC)

## Overview
This project implements a backend service for the **Delivery Order Price Calculator (DOPC)**. Is it a part of a assignment for a backend engineering internship.

---

## Installation

### Prerequisites
- Python 3.9+
- `pip` (Python package manager)

### Steps
1. Unzip the Wolt-Backend.zip folder:
   ```bash
   cd Wolt-Backend
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv env
   source env/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the FastAPI application:
   ```bash
   uvicorn app.main:app --reload
   ```

5. Access the API documentation:
   - Open your browser at `http://127.0.0.1:8000/docs` for interactive Swagger documentation.

---

## API Endpoint
Calculates distance-based delivery fee using a configurable pricing model.
### **GET** `/api/v1/delivery-order-price`

#### Query Parameters
| Parameter  | Type   | Description                                           |
|------------|--------|-------------------------------------------------------|
| venue_slug | string | Unique identifier for the venue                       |
| cart_value | int    | Total value of the items in the shopping cart (in cents)|
| user_lat   | float  | Latitude of the user's location                        |
| user_lon   | float  | Longitude of the user's location                       |

#### Example Request
```
curl "http://localhost:8000/api/v1/delivery-order-price?venue_slug=home-assignment-venue-helsinki&cart_value=1000&user_lat=60.17094&user_lon=24.93087"
```

#### Example Response
```json
{
  "total_price": 1190,
  "small_order_surcharge": 0,
  "cart_value": 1000,
  "delivery": {
    "fee": 190,
    "distance": 177
  }
}
```
