# task3_analysis.py
# TrendPulse:Analyse cleaned data with Pandas + NumPy
# Author: Shashank
# Date: 05-04-2026 

import pandas as pd, numpy as np, os

# Step 1: Load and Explore
fname = "/content/data/trends_clean.csv"
df = pd.read_csv(fname)
print(f"Loaded data: {df.shape}\n")

print("First 5 rows:")
print(df.head(), "\n")

print("Average score   :", df["score"].mean())
print("Average comments:", df["num_comments"].mean())

# Step 2: Basic Analysis with NumPy
scores = df["score"].values

print("\n--- NumPy Stats ---")
print("Mean score   :", np.mean(scores))
print("Median score :", np.median(scores))
print("Std deviation:", np.std(scores))
print("Max score    :", np.max(scores))
print("Min score    :", np.min(scores))

# Category with most stories
cat_counts = df["category"].value_counts()
top_cat = cat_counts.idxmax()
print(f"\nMost stories in: {top_cat} ({cat_counts.max()} stories)")

# Story with most comments
top_story = df.loc[df["num_comments"].idxmax()]
print(f"\nMost commented story: \"{top_story['title']}\" — {top_story['num_comments']} comments")

# Step 3: Add New Columns
avg_score = df["score"].mean()
df["engagement"] = df["num_comments"] / (df["score"] + 1)
df["is_popular"] = df["score"] > avg_score

# Step 4: Save Result
out = "data/trends_analysed.csv"
os.makedirs("data", exist_ok=True)
df.to_csv(out, index=False)

print(f"\nSaved to {out}")
