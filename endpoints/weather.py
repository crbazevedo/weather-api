from fastapi import APIRouter
from services.openweathermap import get_weather_data

router = APIRouter()

@router.get('/weather/{city}')
async def weather(city: str):
    return await get_weather_data(city)
