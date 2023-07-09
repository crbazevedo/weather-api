from fastapi import APIRouter, HTTPException
from .weather import get_weather
from security.transport import HideSensitiveTransport
import httpx
import os
import logging

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.get("/weather-report/{city}")
async def get_weather_report(city: str):
    # use get_weather() function to get weather data
    weather_data = await get_weather(city)
        
    # write report using GPT-4
    gpt4_api_key = os.getenv("OPENAI_API_KEY")
    gpt4_url = "https://api.openai.com/v1/chat/completions"

    prompt = f"""Write a short Weather Report for {city} in the style of a local news reporter based on the following data: {weather_data}. Use the language spoken in that city for the report. Add inside jokes about the city and make it sound like a real weather report. Use regional terms and local idioms when applicable. Write in the style of a local news reporter who is from {city}."""
    headers = {
        "Authorization": f"Bearer {gpt4_api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-4-0613",
        "temperature": 0.1,
        "max_tokens": 1000,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "messages": [
        {
            "role": "user",
            "content": prompt
        }],
    }

    async with httpx.AsyncClient() as client:
        try:
            resp = await client.request("POST", gpt4_url, headers=headers, json=data, timeout=30.0)
            #resp.raise_for_status()
        except httpx.HTTPStatusError as exc:
            logger.error(f"Error fetching OpenAI completion: {exc}")
            raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)
        gpt4_data = resp.json()
        report = gpt4_data["choices"][0]["message"]["content"]
        return {"report": report}
