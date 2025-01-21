from fastapi import FastAPI
from api.v1 import endpoints

app = FastAPI()


@app.get("/")
async def root():
    return {"Wolt 2025 Backend Engineering Internship Assignment"}

app.include_router(endpoints.router, prefix="/api/v1")