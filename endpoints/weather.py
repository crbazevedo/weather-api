from fastapi import APIRouter
from services.openweathermap import get_weather

router = APIRouter()

@router.get('/{city}')
async def weather(city: str):
    return await get_weather(city)
