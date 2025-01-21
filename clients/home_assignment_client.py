import httpx

class HomeAssignmentClient:
    BASE_URL = "https://consumer-api.development.dev.woltapi.com/home-assignment-api/v1"

    async def get_static_data(self, venue_slug: str):
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.BASE_URL}/venues/{venue_slug}/static")
            response.raise_for_status()
            return response.json()

    async def get_dynamic_data(self, venue_slug: str):
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.BASE_URL}/venues/{venue_slug}/dynamic")
            response.raise_for_status()
            return response.json()
