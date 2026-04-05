# task4_visualise.py
# TrendPulse: Make charts from analysed data
# Author: Shashank
# Date: 05-04-2026 

import pandas as pd
import matplotlib.pyplot as plt
import os

# Step 1: Setup
# Load the CSV file from Task 3
df = pd.read_csv("/content/data/trends_analysed.csv")

# Make sure outputs/ folder exists
os.makedirs("outputs", exist_ok=True)

# Step 2: Chart 1 - Top 10 Stories by Score
top10 = df.nlargest(10, "score")   # pick 10 highest scores
# Shorten long titles
titles = [t[:50] + "..." if len(t) > 50 else t for t in top10["title"]]

plt.figure(figsize=(10,6))
plt.barh(titles, top10["score"], color="skyblue")
plt.xlabel("Score")
plt.ylabel("Story Title")
plt.title("Top 10 Stories by Score")
plt.tight_layout()
plt.savefig("outputs/chart1_top_stories.png")
plt.close()

# Step 3: Chart 2 - Stories per Category
cat_counts = df["category"].value_counts()

plt.figure(figsize=(8,6))
plt.bar(cat_counts.index, cat_counts.values,
        color=["blue","green","red","orange","purple"])
plt.xlabel("Category")
plt.ylabel("Number of Stories")
plt.title("Stories per Category")
plt.tight_layout()
plt.savefig("outputs/chart2_categories.png")
plt.close()

# Step 4: Chart 3 - Score vs Comments
colors = df["is_popular"].map({True:"green", False:"red"})

plt.figure(figsize=(8,6))
plt.scatter(df["score"], df["num_comments"], c=colors)
plt.xlabel("Score")
plt.ylabel("Number of Comments")
plt.title("Score vs Comments")
plt.legend(["Popular","Not Popular"])
plt.tight_layout()
plt.savefig("outputs/chart3_scatter.png")
plt.close()

# Bonus: Dashboard (all charts together)
fig, axes = plt.subplots(1, 3, figsize=(18,6))

# Chart 1
axes[0].barh(titles, top10["score"], color="skyblue")
axes[0].set_title("Top 10 by Score")

# Chart 2
axes[1].bar(cat_counts.index, cat_counts.values,
            color=["blue","green","red","orange","purple"])
axes[1].set_title("Stories per Category")

# Chart 3
axes[2].scatter(df["score"], df["num_comments"], c=colors)
axes[2].set_title("Score vs Comments")

fig.suptitle("TrendPulse Dashboard", fontsize=16)
plt.tight_layout()
plt.savefig("outputs/dashboard.png")
plt.close()

print("Charts saved in outputs/ folder:")
print(" - chart1_top_stories.png")
print(" - chart2_categories.png")
print(" - chart3_scatter.png")
print(" - dashboard.png")
