import os
import pandas as pd
import time
import json
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyze_sentiment(text, max_retries=3):
    """
    Analyze sentiment of text using Groq API with retry logic
    Returns: sentiment label and confidence score
    """
    if not text or text.strip() == '':
        return 'neutral', 0.0
    
    for attempt in range(max_retries):
        try:
            message = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "user",
                        "content": f"""Analyze the sentiment of the following text and respond with ONLY a JSON object in this exact format:
{{"sentiment": "positive|negative|neutral", "confidence": 0.0-1.0}}

Text: {text[:500]}"""
                    }
                ],
                temperature=0.3,
                max_tokens=50
            )
            
            response_text = message.choices[0].message.content.strip()
            
            # Parse the response
            try:
                result = json.loads(response_text)
                return result.get('sentiment', 'neutral'), result.get('confidence', 0.0)
            except json.JSONDecodeError:
                # Fallback parsing if JSON is malformed
                if 'positive' in response_text.lower():
                    return 'positive', 0.7
                elif 'negative' in response_text.lower():
                    return 'negative', 0.7
                else:
                    return 'neutral', 0.5
        
        except Exception as e:
            if attempt < max_retries - 1:
                # Wait before retrying (exponential backoff)
                wait_time = 2 ** attempt
                print(f"  Retry in {wait_time}s... (Attempt {attempt + 1}/{max_retries})")
                time.sleep(wait_time)
            else:
                # print(f"  Error after retries: {str(e)[:50]}")
                return 'neutral', 0.0

def analyze_batch_sentiment(texts):
    """
    Analyze sentiment for a batch of texts
    """
    sentiments = []
    confidences = []
    
    for text in texts:
        if pd.isna(text) or (isinstance(text, str) and text.strip() == ''):
            sentiments.append('neutral')
            confidences.append(0.0)
        else:
            sentiment, confidence = analyze_sentiment(str(text))
            sentiments.append(sentiment)
            confidences.append(confidence)
        
        # Add small delay to avoid rate limiting
        time.sleep(0.3)
    
    return sentiments, confidences

def process_sentiment_analysis(input_file, output_file, batch_size=50):
    """
    Process sentiment analysis with batching and progress saving
    """
    try:
        # Read the CSV file
        df = pd.read_csv(input_file)
        
        print(f"Loaded {len(df)} records from {input_file}")
        print(f"Processing in batches of {batch_size}...\n")
        
        # Initialize lists to store results
        sentiments = []
        confidences = []
        
        total_records = len(df)
        
        # Process in batches
        for batch_start in range(0, total_records, batch_size):
            batch_end = min(batch_start + batch_size, total_records)
            batch_texts = df['clean_text'].iloc[batch_start:batch_end].tolist()
            
            print(f"Processing batch {batch_start // batch_size + 1}/{(total_records + batch_size - 1) // batch_size}")
            batch_sentiments, batch_confidences = analyze_batch_sentiment(batch_texts)
            
            sentiments.extend(batch_sentiments)
            confidences.extend(batch_confidences)
            
            print(f"  Completed {batch_end}/{total_records} records\n")
        
        # Add sentiment results to dataframe
        df['sentiment'] = sentiments
        df['confidence'] = confidences
        
        # Save to output file
        df.to_csv(output_file, index=False)
        print(f"Sentiment analysis complete!")
        print(f"Results saved to {output_file}")
        
        # Print summary statistics
        print("\n=== Sentiment Summary ===")
        print(df['sentiment'].value_counts())
        print(f"\nAverage Confidence: {df['confidence'].mean():.2f}")
        print(f"Total Records Processed: {len(df)}")
        
        return df
    
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found")
    except Exception as e:
        print(f"Error processing file: {e}")

if __name__ == "__main__":
    # File paths
    input_csv = r"data\processed\cleaned_text.csv"
    output_csv = r"data\processed\sentiment_analysis_results_batch.csv"
    
    # Run sentiment analysis with batching
    df = process_sentiment_analysis(input_csv, output_csv, batch_size=30)
