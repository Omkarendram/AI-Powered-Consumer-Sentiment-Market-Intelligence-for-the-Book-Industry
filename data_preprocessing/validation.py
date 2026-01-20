import pandas as pd
import numpy as np


# Load data
df = pd.read_csv("data/processed/cleaned_text.csv")
print("Initial shape:", df.shape)
print("Columns found:", df.columns.tolist())

# Standardize column name
if "clean_text" in df.columns:
    df.rename(columns={"clean_text": "cleaned_text"}, inplace=True)

assert "cleaned_text" in df.columns, "Missing 'cleaned_text' column"

print("Validation passed ✅")

print("Initial shape:", df.shape)

print("Columns found:", df.columns.tolist())
print(df.head())

# Check required column
assert "cleaned_text" in df.columns, "Missing 'cleaned_text' column"


# Remove null and empty text
df["cleaned_text"] = df["cleaned_text"].astype(str)
df = df[df["cleaned_text"].str.strip().astype(bool)]


# Drop duplicates
duplicate_count = df.duplicated(subset=["cleaned_text"]).sum()
df = df.drop_duplicates(subset=["cleaned_text"])


# Text length metrics
df["text_length"] = df["cleaned_text"].str.len()


stats = {
"total_rows_after_cleaning": len(df),
"duplicate_rows_removed": duplicate_count,
"min_length": int(df["text_length"].min()),
"max_length": int(df["text_length"].max()),
"avg_length": round(df["text_length"].mean(), 2)
}


print("Validation Summary:")
for k, v in stats.items():
    print(f"{k}: {v}")


# Save validated output
df.drop(columns=["text_length"], inplace=True)
df.to_csv("validated_cleaned_text.csv", index=False)


print("Validated file saved as validated_cleaned_text.csv")