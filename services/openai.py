import json
import httpx
import os
import logging
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv() # load environment variables from .env file

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def generate_weather_report(city: str, weather_data: dict):
    return await generate_report(city, weather_data, 'Weather')

async def generate_news_report(city: str, news_data: dict):
    news_text = await extract_news_text(news_data)
    return await generate_report(city, news_text, 'News')

async def extract_news_text(news_data: dict):
    news_list = []
    for news in news_data['value']:
        if 'video' not in news:
            page_content = await httpx.get(news['url'])
            soup = BeautifulSoup(page_content.text, 'html.parser')
            paragraphs = soup.find_all('p')
            news_text = ''
            for paragraph in paragraphs:
                news_text += paragraph.text + '\n'
            news_item = {
                'headline': news['name'],
                'description': news['description'],
                'provider': news['provider'][0]['name'],
                'datePublished': news['datePublished'],
                'text': news_text
            }
            news_list.append(news_item)
    return json.dumps(news_list)


async def generate_report(city: str, data: str, report_type: str):
    gpt4_api_key = os.getenv("OPENAI_API_KEY")
    gpt4_url = "https://api.openai.com/v1/chat/completions"

    prompt = f"""Write a short {report_type} Report for {city} in the style of a local news reporter based on the following data: {data}. Use the language spoken in that city for the report. Add inside jokes about the city and make it sound like a real {report_type.lower()} report. Use regional terms and local idioms when applicable. Write in the style of a local news reporter who is from {city}. If the news is tragic, you should keep a serious tone. If the news is neutral, you should apply inside jokes and a sense of humor."""
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
        except httpx.HTTPStatusError as exc:
            logger.error(f"Error fetching OpenAI completion: {exc}")
            raise
        gpt4_data = resp.json()
        report = gpt4_data["choices"][0]["message"]["content"]
        return report