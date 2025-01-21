from fastapi import APIRouter, Query, HTTPException
from models.schemas import PriceResponse
from services.delivery_order_service import calculate_delivery_order_price

router = APIRouter()


@router.get("/delivery-order-price", response_model=PriceResponse)
async def delivery_order_price(
        venue_slug: str = Query(...),
        cart_value: int = Query(...),
        user_lat: float = Query(...),
        user_lon: float = Query(...)
):
    return await calculate_delivery_order_price(
        venue_slug=venue_slug,
        cart_value=cart_value,
        user_lat=user_lat,
        user_lon=user_lon
    )
