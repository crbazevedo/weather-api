from fastapi import FastAPI
from dotenv import load_dotenv
import os
import httpx

load_dotenv() # load environment variables from .env file

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/weather/{city}")
async def read_weather(city: str):
    api_key = os.getenv("OPENWEATHER_API_KEY")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        return resp.json()