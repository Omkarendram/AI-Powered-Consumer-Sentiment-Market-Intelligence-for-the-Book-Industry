import requests
import pandas as pd
import time

API_KEY = "d851e72bb7c5472f96b610148face72a"
BASE_URL = "https://newsapi.org/v2/everything"

QUERY = "books OR publishing OR ebook OR reading OR book sales"
PAGE_SIZE = 100
TOTAL_ARTICLES_TARGET = 1000

articles = []
page = 1

while len(articles) < TOTAL_ARTICLES_TARGET:
    params = {
        "q": QUERY,
        "language": "en",
        "pageSize": PAGE_SIZE,
        "page": page,
        "apiKey": API_KEY
    }

    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if data.get("status") != "ok":
        print("Error:", data)
        break

    fetched = data.get("articles", [])
    if not fetched:
        break

    for item in fetched:
        articles.append({
            "title": item.get("title", ""),
            "description": item.get("description", ""),
            "content": item.get("content", ""),
            "source": item.get("source", {}).get("name", ""),
            "published_at": item.get("publishedAt", ""),
            "category": "ecommerce_news"
        })

    print(f"Collected {len(articles)} news articles so far...")
    page += 1
    time.sleep(1)   # polite delay

df = pd.DataFrame(articles)
df.to_csv("data/raw/news_articles.csv", index=False)

print(f"Finished collecting {len(df)} news articles")
