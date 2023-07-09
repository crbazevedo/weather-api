from security.transport import HideSensitiveTransport
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import os
import httpx
import logging
from httpx import AsyncClient
import urllib.parse

load_dotenv() # load environment variables from .env file

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/weather/{city}")
async def read_weather(city: str):
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
    
    
# get read_weather() response and sends to OpenAI API GPT-3 to generate a weather report
@app.get("/weather-report/{city}")
async def read_weather_report(city: str):
    # use read_weather() function to get weather data
    weather_data = await read_weather(city)
        
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

    transport = HideSensitiveTransport(sensitive_params=['gpt4_api_key'])
    async with httpx.AsyncClient(transport=HideSensitiveTransport()) as client:
        try:
            resp = await client.request("POST", gpt4_url, headers=headers, json=data, timeout=30.0)
            resp.raise_for_status()
        except httpx.HTTPStatusError as exc:
            logger.error(f"Error fetching OpenAI completion: {exc}")
            raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)
        gpt4_data = resp.json()
        report = gpt4_data["choices"][0]["message"]["content"]
        return {"report": report}

