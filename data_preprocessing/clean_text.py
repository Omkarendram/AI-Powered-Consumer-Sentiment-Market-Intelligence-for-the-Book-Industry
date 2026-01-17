import pandas as pd
import re
import nltk
from nltk.corpus import stopwords

nltk.download("stopwords")

STOPWORDS = set(stopwords.words("english"))

# -------- TEXT CLEANING FUNCTION --------
def clean_text(text):
    if pd.isna(text):
        return ""

    text = text.lower()
    text = re.sub(r"http\S+", "", text)      # remove URLs
    text = re.sub(r"[^a-z\s]", "", text)     # remove numbers & symbols
    text = re.sub(r"\s+", " ", text).strip() # remove extra spaces

    words = [w for w in text.split() if w not in STOPWORDS]
    return " ".join(words)

# -------- LOAD DATA --------
yt = pd.read_csv("data/raw/youtube_book_comments.csv")
news = pd.read_csv("data/raw/news_articles.csv")

# choose text columns
yt_text = yt["comment_text"]
news_text = news["description"].fillna("") + " " + news["content"].fillna("")

combined_text = pd.concat([yt_text, news_text], ignore_index=True)

# -------- CLEAN --------
cleaned = combined_text.apply(clean_text)

df_clean = pd.DataFrame({"clean_text": cleaned})

# -------- SAVE --------
df_clean.to_csv("data/processed/cleaned_text.csv", index=False)

print(f"Saved {len(df_clean)} cleaned text records")
