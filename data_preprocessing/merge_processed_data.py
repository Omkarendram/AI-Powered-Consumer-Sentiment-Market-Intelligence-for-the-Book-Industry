import pandas as pd

files = [
    "data/processed/cleaned_text.csv",
    "data/processed/sentiment_analysis_results_batch.csv",
    "data/processed/sentiment_analysis_results.csv"
]

dfs = []

for f in files:
    try:
        df = pd.read_csv(f)
        dfs.append(df)
        print(f"Loaded {f} with {len(df)} rows")
    except Exception as e:
        print(f"Could not load {f}: {e}")

final_df = pd.concat(dfs, ignore_index=True)

# Drop duplicates if same clean_text appears multiple times
if "clean_text" in final_df.columns:
    final_df = final_df.drop_duplicates(subset=["clean_text"])

final_df.to_csv("data/processed/final_book_feedback.csv", index=False)
print("✅ final_book_feedback.csv created")
