import math
from fastapi import HTTPException

from clients.home_assignment_client import HomeAssignmentClient
from models.schemas import PriceResponse, Delivery


async def calculate_delivery_order_price(venue_slug: str, cart_value: int, user_lat: float,
                                         user_lon: float) -> PriceResponse:
    # Input validation
    if not venue_slug or not isinstance(venue_slug, str):
        raise HTTPException(status_code=400, detail="Invalid venue_slug, a non-empty string required.")

    if not isinstance(cart_value, int) or cart_value < 0:
        raise HTTPException(status_code=400, detail="Invalid cart_value, a non-negative integer required.")

    if not isinstance(user_lat, float) or not (-90 <= user_lat <= 90):
        raise HTTPException(status_code=400, detail="Invalid user_lat. Valid range between -90 and 90.")

    if not isinstance(user_lon, float) or not (-180 <= user_lon <= 180):
        raise HTTPException(status_code=400, detail="Invalid user_lon. Valid range between -180 and 180.")

    client = HomeAssignmentClient()

    static_data = await client.get_static_data(venue_slug)
    dynamic_data = await client.get_dynamic_data(venue_slug)

    location_of_venue = static_data["venue_raw"]["location"]["coordinates"]
    order_minimum_no_surcharge = dynamic_data["venue_raw"]["delivery_specs"]["order_minimum_no_surcharge"]
    base_price = dynamic_data["venue_raw"]["delivery_specs"]["delivery_pricing"]["base_price"]
    distance_ranges = dynamic_data["venue_raw"]["delivery_specs"]["delivery_pricing"]["distance_ranges"]

    max_distance = distance_ranges[-1]["min"]
    delivery_distance = approximate_distance(user_lat, user_lon, location_of_venue[1], location_of_venue[0])
    small_order_surcharge = max(order_minimum_no_surcharge - cart_value, 0)

    if delivery_distance >= max_distance:
        raise HTTPException(status_code=400,
                            detail=f"Delivery not possible for distances beyond {max_distance} meters.")

    delivery_fee = calculate_delivery_fee(delivery_distance, distance_ranges, base_price)
    total_price = cart_value + small_order_surcharge + delivery_fee

    return PriceResponse(
        total_price=total_price,
        small_order_surcharge=small_order_surcharge,
        cart_value=cart_value,
        delivery=Delivery(
            fee = delivery_fee,
            distance = delivery_distance
        )
    )


def approximate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> int:
    """Approximate straight-line distance between two points in meters."""
    # Approximate conversion factors
    meters_per_degree_latitude = 111_320  # Approximately 111.32 km per degree latitude
    meters_per_degree_longitude = 40075000 * math.cos(math.radians(lat1)) / 360  # Varies by latitude

    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1

    # Approximate Euclidean distance
    distance = math.sqrt((delta_lat * meters_per_degree_latitude) ** 2 +
                         (delta_lon * meters_per_degree_longitude) ** 2)
    return round(distance)

def calculate_delivery_fee(distance: int, distance_ranges: list, base_price: int) -> int:
    """Calculate the delivery fee based on distance."""
    for range_obj in distance_ranges:
        if range_obj["min"] <= distance < range_obj["max"]:
            a = range_obj["a"]
            b = range_obj["b"]
            distance_fee = round(b * distance / 10)
            return base_price + a + distance_fee

