from fastapi import APIRouter
from services.bing_news_search import get_news_data

router = APIRouter()

@router.get('/news_report/{city}')
async def news_report(city: str):
    return await get_news_data(city)
