from fastapi import FastAPI
from endpoints import weather, weather_report, news_report

app = FastAPI()

app.include_router(weather.router)
app.include_router(weather_report.router)
app.include_router(news_report.router)