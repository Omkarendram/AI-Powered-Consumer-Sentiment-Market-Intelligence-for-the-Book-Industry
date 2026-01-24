# Sentiment Analysis Using Groq API

This project performs sentiment analysis on your cleaned text data using the Groq API.

## Setup Instructions

### 1. Prerequisites
- Python 3.8+
- Groq API Key (Get from https://console.groq.com/keys)

### 2. Installation

Install required packages:
```bash
pip install -r requirements.txt
```

### 3. Configuration

Create a `.env` file in the project root with your Groq API key:
```
GROQ_API_KEY=your_api_key_here
```

## Scripts

### `sentiment_analysis.py` (Recommended for smaller datasets)
- Processes records sequentially with 0.5s delay between API calls
- Includes retry logic with exponential backoff for rate limiting
- Progress updates every 10 records
- Output: `data/processed/sentiment_analysis_results.csv`

**Run:**
```bash
python sentiment_analysis.py
```

**Estimated Time:** ~3 minutes for 344 records

### `sentiment_analysis_batch.py` (For larger datasets)
- Processes records in configurable batches (default: 30 records per batch)
- Better error handling and progress tracking
- Output: `data/processed/sentiment_analysis_results_batch.csv`

**Run:**
```bash
python sentiment_analysis_batch.py
```

## How It Works

1. **Input:** Reads cleaned text from `data/processed/cleaned_text.csv`
2. **Analysis:** Sends each text to Groq's LLM (Llama 3.3 70B) with sentiment analysis prompt
3. **Output:** Returns 3 columns:
   - `clean_text`: Original cleaned text
   - `sentiment`: One of `positive`, `negative`, or `neutral`
   - `confidence`: Confidence score (0.0 - 1.0)

## Output Format

The output CSV contains the original data plus sentiment analysis:
```
clean_text,sentiment,confidence
"some text here",positive,0.85
"another text",negative,0.92
...
```

## Rate Limiting Notes

- Groq free tier has rate limits (typically 30 requests per minute)
- The scripts include automatic retries with exponential backoff
- Use 0.3-0.5 second delays between requests to avoid hitting limits
- For large-scale analysis, consider using Groq's paid tier

## Sentiment Analysis Details

- **Model:** Llama 3.3 70B Versatile
- **Prompt:** Analyzes text for positive, negative, or neutral sentiment
- **JSON Response:** Returns structured JSON with sentiment and confidence

## Troubleshooting

### Rate Limiting (429 Error)
- Increase the delay in `time.sleep()` calls
- Try running in batches with longer delays between batches

### Model Decommissioned Error
- Check available models at https://console.groq.com/docs/models
- Update the `model` parameter in the script

### Empty Results
- Check that your `.env` file has a valid `GROQ_API_KEY`
- Verify the input CSV path is correct

## Example Output

```
sentiment
neutral    344
Name: count, dtype: int64

Average Confidence: 0.75
```

## License

This project is part of the AI Consumer Sentiment Data Collection initiative.
