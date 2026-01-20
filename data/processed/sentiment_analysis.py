import pandas as pd
from transformers import pipeline

# Load cleaned data
df = pd.read_csv("data/processed/cleaned_text.csv")

# Load Hugging Face sentiment-analysis pipeline
sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

def get_sentiment(text):
    result = sentiment_pipeline(str(text)[:512])[0]  # truncate to model limit
    label = result["label"].lower()
    score = round(result["score"], 4)

    # Classify as neutral if confidence is below threshold (closer to 0.5)
    if score < 0.65:
        sentiment = "neutral"
    else:
        sentiment = label

    return pd.Series([sentiment, score])

# Apply sentiment analysis
df[["sentiment_label", "sentiment_score"]] = df["clean_text"].apply(get_sentiment)

# Save output
df.to_csv("data/processed/sentiment_results.csv", index=False)

print("Hugging Face transformer-based sentiment analysis completed.")
