import os
import csv
import pandas as pd
import json
import time
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyze_sentiment(text, retry_count=0, max_retries=5):
    """
    Analyze sentiment with aggressive rate limiting and retry logic
    """
    if not text or str(text).strip() == '':
        return 'neutral', 0.0
    
    if retry_count > 0:
        # Exponential backoff: 2^retry_count seconds
        wait_time = min(2 ** retry_count, 60)  # Cap at 60 seconds
        print(f"    Waiting {wait_time}s before retry {retry_count}/{max_retries}...", end='', flush=True)
        time.sleep(wait_time)
        print(" Done")
    
    try:
        message = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": f"""Respond with ONLY valid JSON (no markdown, no code blocks):
{{"sentiment": "positive|negative|neutral", "confidence": 0.0-1.0}}

Text: {str(text)[:300]}"""
                }
            ],
            temperature=0.2,
            max_tokens=30
        )
        
        response_text = message.choices[0].message.content.strip()
        
        # Clean response (remove markdown if present)
        if response_text.startswith('```'):
            response_text = response_text.split('\n', 1)[1]
        if response_text.endswith('```'):
            response_text = response_text.rsplit('\n', 1)[0]
        
        try:
            result = json.loads(response_text)
            sentiment = result.get('sentiment', 'neutral').lower()
            confidence = float(result.get('confidence', 0.0))
            
            # Validate sentiment value
            if sentiment not in ['positive', 'negative', 'neutral']:
                sentiment = 'neutral'
            
            return sentiment, confidence
        except (json.JSONDecodeError, ValueError):
            # Fallback: parse sentiment from text
            response_lower = response_text.lower()
            if 'positive' in response_lower:
                return 'positive', 0.7
            elif 'negative' in response_lower:
                return 'negative', 0.7
            else:
                return 'neutral', 0.5
    
    except Exception as e:
        error_str = str(e)
        if '429' in error_str or 'Too Many Requests' in error_str:
            if retry_count < max_retries:
                return analyze_sentiment(text, retry_count + 1, max_retries)
            else:
                print(f"    Max retries exceeded")
                return 'neutral', 0.0
        else:
            print(f"    Error: {type(e).__name__}")
            return 'neutral', 0.0

def sentiment_analysis_csv(input_file, output_file):
    """
    Read CSV file, analyze sentiment for each row, and save results
    """
    try:
        # Read the CSV file
        df = pd.read_csv(input_file)
        
        print(f"\nLoaded {len(df)} records from {input_file}")
        print(f"Starting sentiment analysis...\n")
        
        # Initialize lists to store results
        sentiments = []
        confidences = []
        
        # Process each text
        for idx, text in enumerate(df['clean_text'], 1):
            # Handle NaN and empty values
            if pd.isna(text) or str(text).strip() == '':
                sentiments.append('neutral')
                confidences.append(0.0)
                status = "EMPTY"
            else:
                text_preview = str(text)[:45]
                print(f"[{idx:3d}/{len(df)}] {text_preview}...", end=' ', flush=True)
                sentiment, confidence = analyze_sentiment(str(text))
                sentiments.append(sentiment)
                confidences.append(confidence)
                status = f"{sentiment.upper()} ({confidence:.2f})"
                print(f"→ {status}")
            
            # Add 2-3 second delay between ALL requests to avoid rate limiting
            time.sleep(2.5)
        
        # Add sentiment results to dataframe
        df['sentiment'] = sentiments
        df['confidence'] = confidences
        
        # Save to output file
        df.to_csv(output_file, index=False)
        print(f"\n✓ Sentiment analysis complete!")
        print(f"✓ Results saved to {output_file}")
        
        # Print summary statistics
        print("\n" + "="*50)
        print("SENTIMENT SUMMARY")
        print("="*50)
        print(df['sentiment'].value_counts())
        print(f"\nAverage Confidence: {df['confidence'].mean():.2f}")
        print(f"Total Records: {len(df)}")
        
        return df
    
    except FileNotFoundError:
        print(f"✗ Error: Input file '{input_file}' not found")
    except Exception as e:
        print(f"✗ Error: {e}")

if __name__ == "__main__":
    # File paths (using absolute paths)
    base_dir = r"c:\Users\KIIT0001\Downloads\infosys\infosys\ai-consumer-sentiment-data-collection"
    input_csv = f"{base_dir}\\data\\processed\\cleaned_text.csv"
    output_csv = f"{base_dir}\\data\\processed\\sentiment_analysis_results.csv"
    
    print("=" * 60)
    print("SENTIMENT ANALYSIS WITH GROQ API")
    print("=" * 60)
    
    # Run sentiment analysis
    df = sentiment_analysis_csv(input_csv, output_csv)
