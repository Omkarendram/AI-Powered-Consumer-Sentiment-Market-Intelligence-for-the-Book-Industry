import requests
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = "https://books.toscrape.com/"

response = requests.get(BASE_URL)
soup = BeautifulSoup(response.text, "html.parser")

books = []

for book in soup.select("article.product_pod"):
    title = book.h3.a["title"]
    price = book.select_one(".price_color").get_text(strip=True)
    rating = book.select_one("p.star-rating")["class"][1]

    books.append({
        "title": title,
        "price": price,
        "rating": rating,
        "category": "books",
        "source": "books.toscrape"
    })

df = pd.DataFrame(books)
df.to_csv("data/raw/ecommerce_books.csv", index=False)

print(f"Collected {len(df)} books from demo e-commerce site")
