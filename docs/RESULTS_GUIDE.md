# 📊 Sentiment Analysis Results - Quick Reference

## ✅ Analysis Complete!

**Date:** January 24, 2026  
**Status:** All 344 reviews analyzed successfully

---

## 📍 Results Location

```
data/processed/sentiment_analysis_results.csv
```

**File Size:** 45.6 KB  
**Records:** 344 reviews

---

## 📈 Key Findings

| Sentiment | Count | Percentage |
|-----------|-------|-----------|
| **Positive** | 147 | **42.73%** ✅ |
| **Negative** | 96 | 27.91% ⚠️ |
| **Neutral** | 101 | 29.36% ℹ️ |

---

## 📊 Confidence Metrics

| Metric | Score |
|--------|-------|
| **Mean Confidence** | **0.74** / 1.0 |
| **Median** | 0.80 |
| **Std Dev** | 0.17 |
| **Range** | 0.00 - 1.00 |

### By Sentiment Type:
- ✅ **Positive Reviews:** 0.81 avg (Very Reliable)
- ⚠️ **Negative Reviews:** 0.78 avg (Very Reliable)
- ℹ️ **Neutral Reviews:** 0.60 avg (Moderately Reliable)

---

## 🗂️ File Organization

```
sentiment_analysis/
├── README.md                          # Detailed documentation
├── sentiment_analysis.py              # Main script (sequential)
├── sentiment_analysis_batch.py        # Batch processing script
├── show_results_summary.py            # Summary statistics
└── test_groq_connection.py            # API test utility

data/processed/
├── cleaned_text.csv                   # Input data
└── sentiment_analysis_results.csv     # ⭐ RESULTS
```

---

## 🚀 How to Use Results

### 1. View Summary Stats
```bash
cd sentiment_analysis
python show_results_summary.py
```

### 2. Load in Python
```python
import pandas as pd

df = pd.read_csv('data/processed/sentiment_analysis_results.csv')

# Get positive reviews
positive = df[df['sentiment'] == 'positive']
print(f"Found {len(positive)} positive reviews")

# Get average confidence per sentiment
print(df.groupby('sentiment')['confidence'].mean())
```

### 3. Filter High-Confidence Results
```python
high_confidence = df[df['confidence'] >= 0.8]
print(f"High confidence results: {len(high_confidence)}")
```

### 4. Export Specific Sentiments
```python
# Export only positive reviews
df[df['sentiment'] == 'positive'].to_csv('positive_reviews.csv', index=False)
```

---

## 📊 Interpretation Guide

| Sentiment | Confidence | Meaning |
|-----------|-----------|---------|
| Positive | 0.80+ | Strong positive sentiment |
| Positive | 0.70-0.80 | Likely positive |
| Positive | <0.70 | Weakly positive |
| Negative | 0.80+ | Strong negative sentiment |
| Negative | 0.70-0.80 | Likely negative |
| Negative | <0.70 | Weakly negative |
| Neutral | 0.60-0.80 | Mixed/Unclear sentiment |
| Neutral | <0.60 | Very ambiguous |

---

## 💡 Key Insights

1. **Majority Positive:** 42.73% of reviews are positive
2. **Balanced Critical Feedback:** 27.91% negative reviews provide valuable critical perspective
3. **Clear Signals:** 70.64% of reviews show clear sentiment (positive or negative)
4. **High Reliability:** 74% average confidence across all predictions
5. **Strong Positive Sentiment:** Positive reviews are most confidently identified (0.81)

---

## 🔄 Re-running Analysis

### Update Input Data
If you add new reviews to `data/processed/cleaned_text.csv`:

```bash
cd sentiment_analysis
python sentiment_analysis.py        # For small updates
# or
python sentiment_analysis_batch.py  # For large updates
```

### Compare Results
```bash
# Old results backup
cp data/processed/sentiment_analysis_results.csv data/processed/sentiment_analysis_results_backup.csv

# Run new analysis
python sentiment_analysis/sentiment_analysis.py
```

---

## 🛠️ Troubleshooting

### Results Not Updating?
1. Check `.env` has valid `GROQ_API_KEY`
2. Run test: `python sentiment_analysis/test_groq_connection.py`
3. Verify internet connection
4. Check Groq rate limits: https://console.groq.com

### Low Confidence Scores?
- Normal for ambiguous/neutral reviews
- Consider 0.60+ as acceptable confidence
- Very low scores (<0.40) may indicate review text is too short/unclear

### Need Different Model?
- Update `sentiment_analysis.py` line 25
- Available models: https://console.groq.com/docs/models
- Update rate limiting if using slower model

---

## 📞 Next Steps

1. **Visualize:** Create charts of sentiment distribution
2. **Export:** Share results in specific formats (JSON, Excel, etc.)
3. **Filter:** Extract high-confidence results for quality analysis
4. **Integrate:** Use results for recommendation systems
5. **Monitor:** Track sentiment trends over time with new reviews

---

**Analysis Tool:** Groq API (Llama 3.3 70B)  
**Processing Time:** ~15 minutes  
**Cost:** Free tier (Groq API)  
**Quality:** 74% average confidence  

✅ **Ready to use!**
