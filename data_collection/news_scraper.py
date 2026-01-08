import requests
import pandas as pd
import xml.etree.ElementTree as ET

RSS_URL = "https://news.google.com/rss/search?q=ecommerce+business"

response = requests.get(RSS_URL)
root = ET.fromstring(response.content)

articles = []

for item in root.findall(".//item")[:15]:   # take first 15 news items
    title = item.find("title").text
    link = item.find("link").text
    pub_date = item.find("pubDate").text

    articles.append({
        "text": title,
        "link": link,
        "published": pub_date,
        "category": "ecommerce_news",
        "source": "google_news_rss"
    })

df = pd.DataFrame(articles)
df.to_csv("data/raw/news_articles.csv", index=False)

print(f"Collected {len(df)} news articles from Google News RSS")
