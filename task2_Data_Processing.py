# task2_clean_data.py
# TrendPulse: Clean raw JSON into tidy CSV
# Author: Shashank
# Date: YYYY-MM-DD

import pandas as pd, json, os

# --- Step 1: Load JSON file ---
fname = "/content/data/trends_20260405.json"   
with open(fname) as f:
    raw = json.load(f)

df = pd.DataFrame(raw)
print(f"Loaded {len(df)} stories from {fname}")

# --- Step 2: Clean the Data ---

# Remove duplicates by post_id
df = df.drop_duplicates(subset="post_id")
print("After removing duplicates:", len(df))

# Drop rows with missing post_id, title, or score
df = df.dropna(subset=["post_id","title","score"])
print("After removing nulls:", len(df))

# Ensure score and num_comments are integers
df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].astype(int)

# Remove low quality (score < 5)
df = df[df["score"] >= 5]
print("After removing low scores:", len(df))

# Strip whitespace from titles
df["title"] = df["title"].str.strip()

# --- Step 3: Save as CSV ---
out = "data/trends_clean.csv"
os.makedirs("data", exist_ok=True)
df.to_csv(out, index=False)

print(f"\nSaved {len(df)} rows to {out}\n")

# Quick summary: stories per category
print("Stories per category:")
print(df["category"].value_counts())
