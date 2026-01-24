import os
import pandas as pd
from groq import Groq

# Initialize Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Load cleaned text data
df = pd.read_csv("data/processed/cleaned_text.csv")
texts = df["clean_text"].dropna().tolist()

# Function to batch texts
def batch_texts(texts, batch_size=5):
    for i in range(0, len(texts), batch_size):
        yield texts[i:i + batch_size]

results = []

for idx, batch in enumerate(batch_texts(texts, batch_size=5)):
    numbered_texts = "\n".join([f"{i+1}. {text}" for i, text in enumerate(batch)])

    prompt = f"""
You are an NLP expert.

Given the following customer texts:
{numbered_texts}

Identify ONE main topic discussed.
Extract 5 important keywords.

Return output exactly in this format:
Topic:
Keywords:
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    results.append({
        "batch_id": idx,
        "llm_output": response.choices[0].message.content.strip()
    })

# Save LLM topic modeling results
pd.DataFrame(results).to_csv("llm_topic_results.csv", index=False)