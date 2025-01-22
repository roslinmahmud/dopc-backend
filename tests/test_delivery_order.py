import pytest
from unittest.mock import AsyncMock, patch
from fastapi import HTTPException
from clients.home_assignment_client import HomeAssignmentClient
from models.schemas import PriceResponse
from services.delivery_order_service import calculate_delivery_order_price

@pytest.mark.asyncio
async def test_calculate_delivery_order_price_success():
    # Mock static and dynamic data responses
    static_data = {
        "venue_raw": {
            "location": {
                "coordinates": [24.93545, 60.16952]
            }
        }
    }

    dynamic_data = {
        "venue_raw": {
            "delivery_specs": {
                "order_minimum_no_surcharge": 1000,
                "delivery_pricing": {
                    "base_price": 500,
                    "distance_ranges": [
                        {"min": 0, "max": 1000, "a": 100, "b": 2},
                        {"min": 1000, "max": 0, "a": 0, "b": 0}
                    ]
                }
            }
        }
    }

    with patch.object(HomeAssignmentClient, 'get_static_data', new=AsyncMock(return_value=static_data)), \
         patch.object(HomeAssignmentClient, 'get_dynamic_data', new=AsyncMock(return_value=dynamic_data)):

        result = await calculate_delivery_order_price("test_venue", 800, 60.17094, 24.93087)

        assert isinstance(result, PriceResponse)
        assert result.total_price > 0
        assert result.small_order_surcharge == 200  # Expected since cart_value < order_minimum_no_surcharge
        assert result.cart_value == 800


@pytest.mark.asyncio
async def test_calculate_delivery_order_price_delivery_not_possible():
    static_data = {
        "venue_raw": {
            "location": {
                "coordinates": [24.93545, 1000]
            }
        }
    }

    dynamic_data = {
        "venue_raw": {
            "delivery_specs": {
                "order_minimum_no_surcharge": 1000,
                "delivery_pricing": {
                    "base_price": 500,
                    "distance_ranges": [
                        {"min": 0, "max": 1000, "a": 200, "b": 2},
                        {"min": 1000, "max": 0, "a": 0, "b": 0}
                    ]
                }
            }
        }
    }

    mock_static_data = AsyncMock(return_value=static_data)
    mock_dynamic_data = AsyncMock(side_effect=HTTPException(status_code=400, detail="Bad Request"))
    user_latitude = 60.17094
    user_longitude = 24.93087

    with patch.object(HomeAssignmentClient, 'get_static_data', new=mock_static_data), \
            patch.object(HomeAssignmentClient, 'get_dynamic_data', new=mock_dynamic_data):

        try:
            result = await calculate_delivery_order_price("test_venue", cart_value=800, user_lat=user_latitude,
                                                          user_lon=user_longitude)
        except HTTPException as exc:
            assert exc.status_code == 400
            assert exc.detail == "Bad Request"
        else:
            raise AssertionError("Expected HTTPException but it was not raised")