from fastapi import FastAPI
from endpoints import weather, weather_report

app = FastAPI()

app.include_router(weather.router)
app.include_router(weather_report.router)