from fastapi import APIRouter
from services.bing_news_search import get_news_data
from services.openai import generate_news_report

router = APIRouter()

@router.get('/news_report/{city}')
async def news_report(city: str):
    news_data = await get_news_data(city)
    return await generate_news_report(city, news_data)
