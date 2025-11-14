# backend/news_api.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def fetch_news_data(keyword, language="en", page_size=10):
    url = f"https://newsapi.org/v2/everything?q={keyword}&language={language}&pageSize={page_size}&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    data = response.json()

    if data.get("status") != "ok":
        print("Error fetching news:", data)
        return []

    articles = data.get("articles", [])
    results = []

    for article in articles:
        results.append({
            "title": article["title"],
            "description": article["description"],
            "url": article["url"],
            "source": article["source"]["name"],
            "publishedAt": article["publishedAt"]
        })

    return results
