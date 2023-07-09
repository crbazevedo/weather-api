from fastapi import APIRouter, HTTPException
from services.openweathermap import get_weather_data
from services.openai import generate_weather_report

router = APIRouter()

@router.get('/weather_report/{city}')
async def weather_report(city: str):
    try:
        weather_data = await get_weather_data(city)
        report = generate_weather_report(city, weather_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {'report': report}
