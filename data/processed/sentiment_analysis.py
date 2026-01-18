import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

# Download VADER lexicon (only first time)
nltk.download('vader_lexicon', quiet=True)

# Load cleaned data
df = pd.read_csv("cleaned_text.csv")

# Initialize sentiment analyzer
sia = SentimentIntensityAnalyzer()

# Function to get sentiment label
def get_sentiment(text):
    score = sia.polarity_scores(str(text))['compound']
    if score >= 0.05:
        return "positive"
    elif score <= -0.05:
        return "negative"
    else:
        return "neutral"

# Apply sentiment analysis
df["sentiment_score"] = df["clean_text"].apply(
    lambda x: sia.polarity_scores(str(x))['compound']
)

df["sentiment_label"] = df["clean_text"].apply(get_sentiment)

# Save results
df.to_csv("sentiment_results.csv", index=False)

print("Sentiment analysis completed. File saved as sentiment_results.csv")
