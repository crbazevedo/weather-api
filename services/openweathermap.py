from security.transport import HideSensitiveTransport
from fastapi import HTTPException
import httpx
import os
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def get_weather(city: str):
    api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key
    }  
    transport = HideSensitiveTransport(sensitive_params=['appid'])

    async with httpx.AsyncClient(transport=transport) as client:
        try:
            resp = await client.request("GET", url, params=params)
            resp.raise_for_status()
        except httpx.HTTPStatusError as exc:
            logger.error(f"Error fetching weather: {exc}")
            raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)

        return resp.json()
