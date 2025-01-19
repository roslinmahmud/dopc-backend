from fastapi import APIRouter, Query, HTTPException
from models.schemas import PriceResponse

router = APIRouter()


@router.get("/delivery-order-price", response_model=PriceResponse)
async def delivery_order_price(
        venue_slug: str = Query(...),
        cart_value: int = Query(...),
        user_lat: float = Query(...),
        user_lon: float = Query(...)
):
    return {
        "total_price": 1190,
        "small_order_surcharge": 0,
        "cart_value": 1000,
        "delivery": {
            "fee": 190,
            "distance": 177
        }
    }
