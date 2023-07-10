import os
import httpx
from typing import Any
from utils import city_to_language_code
from fastapi import HTTPException
from security.transport import HideSensitiveTransport


async def get_news_data(city: str) -> Any:
    api_key = os.getenv("BING_NEWS_SEARCH_API_KEY")
    url = "https://api.bing.microsoft.com/v7.0/news/search"
    params = {
        "q": f"{city}",
        "count": 3,
        "mkt": city_to_language_code(city),
        "safeSearch": "Moderate"
    }
    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
    }
    transport = HideSensitiveTransport(sensitive_params=['Ocp-Apim-Subscription-Key'])

    async with httpx.AsyncClient(transport=transport) as client:
        try:
            resp = await client.get(url, params=params, headers=headers)
            resp.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)

        return resp.json()
