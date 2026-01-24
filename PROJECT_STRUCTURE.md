# AI Consumer Sentiment Data Collection

A comprehensive project for collecting, cleaning, analyzing, and modeling consumer sentiment data from multiple sources (e-commerce, news, YouTube comments).

## 📁 Project Structure

```
ai-consumer-sentiment-data-collection/
├── README.md                              # This file
├── requirements.txt                       # Python dependencies
├── .env                                   # API keys (add your GROQ_API_KEY here)
├── .env.example                           # Template for environment variables
│
├── data/                                  # All data files
│   ├── raw/                               # Original data from sources
│   │   ├── ecommerce_books.csv           # E-commerce book reviews
│   │   ├── news_articles.csv             # News articles
│   │   └── youtube_book_comments.csv     # YouTube comments
│   │
│   └── processed/                         # Cleaned and analyzed data
│       ├── cleaned_text.csv              # Preprocessed text
│       └── sentiment_analysis_results.csv # Sentiment analysis output (⭐ MAIN RESULTS)
│
├── data_collection/                       # Scripts for collecting data
│   ├── ecommerce_scraper.py              # E-commerce scraper
│   ├── news_scraper.py                   # News scraper
│   ├── youtube_comments_collector.py     # YouTube comments collector
│   └── test_imports.py                   # Test imports
│
├── data_preprocessing/                    # Data cleaning scripts
│   ├── clean_text.py                     # Text preprocessing
│   └── validation.py                     # Data validation
│
├── topic_modeling/                        # Topic modeling scripts
│   ├── topic_modeling.py                 # LDA/NMF topic modeling
│   └── topic_results.csv                 # Topic modeling results
│
└── sentiment_analysis/                    # ⭐ Sentiment analysis (NEW)
    ├── README.md                          # Detailed sentiment analysis docs
    ├── sentiment_analysis.py              # Main sentiment analysis script
    ├── sentiment_analysis_batch.py        # Batch processing version
    ├── show_results_summary.py            # Results summary generator
    └── test_groq_connection.py            # API connection test
```

## 🎯 Sentiment Analysis Results

**Location:** `data/processed/sentiment_analysis_results.csv`

### Key Statistics:
- **Total Reviews:** 344
- **Positive:** 147 (42.73%)
- **Negative:** 96 (27.91%)
- **Neutral:** 101 (29.36%)
- **Average Confidence:** 0.74/1.0

### Output Format:
```csv
clean_text,sentiment,confidence
"Review text here",positive,0.90
"Another review",negative,0.85
...
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Add Groq API Key
Create `.env` file (or edit existing):
```
GROQ_API_KEY=your_api_key_here
```
Get free API key: https://console.groq.com/keys

### 3. Run Sentiment Analysis
```bash
cd sentiment_analysis
python sentiment_analysis.py
```

### 4. View Results
```bash
python show_results_summary.py
```

Results will be saved to: `data/processed/sentiment_analysis_results.csv`

## 📊 Data Pipeline

```
Raw Data → Data Collection → Data Preprocessing → Sentiment Analysis → Results
   ↓            ↓                    ↓                    ↓              ↓
data/raw    data_collection      clean_text.csv    Groq API       CSV Output
ecommerce   scrapers & YouTube    validation.py    LLM Analysis   Visualizations
news, etc.  collectors            text_clean.py    Confidence     Reports
```

## 📝 Files Overview

### Data Collection
- `data_collection/ecommerce_scraper.py` - Scrapes e-commerce book reviews
- `data_collection/news_scraper.py` - Collects news articles
- `data_collection/youtube_comments_collector.py` - Extracts YouTube comments

### Data Preprocessing
- `data_preprocessing/clean_text.py` - Text cleaning and normalization
- `data_preprocessing/validation.py` - Data quality validation

### Sentiment Analysis
- `sentiment_analysis/sentiment_analysis.py` - Main script with sequential processing
- `sentiment_analysis/sentiment_analysis_batch.py` - Batch processing for large datasets
- `sentiment_analysis/show_results_summary.py` - Generate summary statistics
- `sentiment_analysis/test_groq_connection.py` - Test API connectivity

### Topic Modeling
- `topic_modeling/topic_modeling.py` - LDA/NMF implementations
- `topic_results.csv` - Topic modeling outputs

## 🔧 Dependencies

Key packages:
- `pandas` - Data manipulation
- `groq` - Groq API client for sentiment analysis
- `scikit-learn` - Machine learning utilities
- `beautifulsoup4` - Web scraping
- `requests` - HTTP requests
- `python-dotenv` - Environment variable management

## 📈 Sentiment Analysis Details

### Model: Llama 3.3 70B (via Groq API)
- **Sentiment Classes:** Positive, Negative, Neutral
- **Confidence:** 0.0 - 1.0 scale
- **Processing Time:** ~2.5 seconds per review
- **Total Time:** ~15 minutes for 344 reviews
- **Rate Limiting:** 2.5s delay between requests

### Performance Metrics
- **Positive Reviews:** Mean confidence 0.81
- **Negative Reviews:** Mean confidence 0.78
- **Neutral Reviews:** Mean confidence 0.60

## 🔐 Environment Variables

Required:
- `GROQ_API_KEY` - Your Groq API key for LLM analysis

Optional:
- `GROQ_MODEL` - Model name (default: llama-3.3-70b-versatile)
- `BATCH_SIZE` - Batch processing size (default: 30)

## 📚 Usage Examples

### Run Full Sentiment Analysis
```bash
cd sentiment_analysis
python sentiment_analysis.py
```

### Run Batch Processing
```bash
cd sentiment_analysis
python sentiment_analysis_batch.py
```

### View Summary Statistics
```bash
cd sentiment_analysis
python show_results_summary.py
```

### Test API Connection
```bash
cd sentiment_analysis
python test_groq_connection.py
```

## 🐛 Troubleshooting

### Rate Limiting (429 Error)
- Increase delay in script: `time.sleep(3)` instead of `time.sleep(2.5)`
- Use batch processing with longer delays
- Check Groq API limits at https://console.groq.com

### Model Decommissioned
- Check available models: https://console.groq.com/docs/models
- Update `model` parameter in sentiment_analysis.py

### File Not Found
- Ensure you're running scripts from project root
- Check file paths in scripts (use absolute paths if needed)

## 📖 Additional Resources

- [Groq API Documentation](https://console.groq.com/docs)
- [Project README](README.md)
- [Sentiment Analysis README](sentiment_analysis/README.md)

## 📄 Output Format

### sentiment_analysis_results.csv
Contains 344 rows (one per review) with columns:
1. `clean_text` - Preprocessed review text
2. `sentiment` - One of: positive, negative, neutral
3. `confidence` - Confidence score (0.0-1.0)

### Example Rows:
```csv
clean_text,sentiment,confidence
dear maam im writing book...,positive,0.90
atomic habits really good...,positive,0.80
found atomic habits boring,negative,0.80
book recommendation here,neutral,0.70
```

## 🎓 Project Insights

- **Most Common Sentiment:** Positive (42.73%)
- **Strongest Agreement:** Negative reviews (0.78 avg confidence)
- **Weaker Signals:** Neutral reviews (0.60 avg confidence)
- **Overall Quality:** High (0.74 avg confidence across all reviews)

This suggests that when readers express strong opinions (positive/negative), the LLM is highly confident, but neutral sentiment signals are less clear—which is expected as neutrality is inherently ambiguous.

## 📞 Support

For issues or questions:
1. Check troubleshooting section above
2. Verify .env file has correct API key
3. Run `test_groq_connection.py` to diagnose API issues
4. Check Groq console for rate limit status

---

**Last Updated:** January 24, 2026  
**Project Status:** ✅ Sentiment Analysis Complete
