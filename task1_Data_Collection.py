# task1_data_collection.py
# TrendPulse: Fetch trending HackerNews stories and categorize them
# Author: Shashank
# Date: 05-04-2026

import requests, json, os, time
from datetime import datetime

# --- Config ---
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"
HEADERS = {"Shashank": "TrendPulse/1.0"}

# Keywords for categories
CATEGORIES = {
    "technology": ["AI","software","tech","code","computer","data","cloud","API","GPU","LLM"],
    "worldnews": ["war","government","country","president","election","climate","attack","global"],
    "sports": ["NFL","NBA","FIFA","sport","game","team","player","league","championship"],
    "science": ["research","study","space","physics","biology","discovery","NASA","genome"],
    "entertainment": ["movie","film","music","Netflix","game","book","show","award","streaming"]
}

# --- Helper: assign category based on title ---
def get_category(title):
    t = title.lower()
    for cat, words in CATEGORIES.items():
        if any(w.lower() in t for w in words):
            return cat
    return None

# --- Step 1: Fetch top story IDs ---
try:
    ids = requests.get(TOP_STORIES_URL, headers=HEADERS, timeout=10).json()[:500]
except Exception as e:
    print("Error fetching top stories:", e)
    ids = []

# --- Step 2: Keep fetching until minimum stories are collected ---
stories = []
total_collected = 0
MIN_STORIES = 120

while total_collected < MIN_STORIES and ids:
    for cat in CATEGORIES:
        count = 0
        for sid in ids:
            if count >= 25: break
            if total_collected >= MIN_STORIES: break
            try:
                response = requests.get(ITEM_URL.format(sid), headers=HEADERS, timeout=10)
                story = response.json()
                if not story or "title" not in story:
                    continue
                category = get_category(story["title"])
                if category == cat:
                    stories.append({
                        "post_id": story.get("id"),
                        "title": story.get("title"),
                        "category": category,
                        "score": story.get("score",0),
                        "num_comments": story.get("descendants",0),
                        "author": story.get("by"),
                        "collected_at": datetime.now().isoformat()
                    })
                    count += 1
                    total_collected += 1
            except Exception as e:
                print(f"Failed to fetch story {sid}: {e}")
        time.sleep(2)  # wait per category

    # If still not enough, wait and retry
    if total_collected < MIN_STORIES:
        print(f"Collected {total_collected} so far, retrying to reach {MIN_STORIES}...")
        time.sleep(5)

# --- Step 3: Save to JSON file ---
os.makedirs("data", exist_ok=True)
fname = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"
with open(fname, "w") as f:
    json.dump(stories, f, indent=2)

print(f"Collected {len(stories)} stories (minimum {MIN_STORIES}). Saved to {fname}")
