import json
import pandas as pd

# --- Load JSON file ---
with open("reliance_daily.json", "r") as f:
    data = json.load(f)

# Extract time series data
time_series = data.get("Time Series (Daily)", {})
df_reliance = pd.DataFrame.from_dict(time_series, orient="index")

# Rename columns for clarity
df_reliance.columns = ["open", "high", "low", "close", "volume"]

# Convert index to datetime
df_reliance.index = pd.to_datetime(df_reliance.index)

# Convert numeric columns to appropriate types
df_reliance = df_reliance.astype({
    "open": float,
    "high": float,
    "low": float,
    "close": float,
    "volume": int
})

# Sort by date
df_reliance.sort_index(inplace=True)

# --- Data Shape Before Cleaning ---
print("Data shape before cleaning:", df_reliance.shape)

# --- Data Cleaning ---
# 1. Identify null values
null_counts = df_reliance.isnull().sum()

# Extra check: if no nulls, print a clear message
if null_counts.sum() == 0:
    print(" No null values found in the dataset.")
else:
    print(" Null values detected, cleaning required.")

print("Null values per column:")
print(null_counts)


# 2. Drop rows with any null values
df_reliance.dropna(inplace=True)

# 3. Drop duplicate rows
df_reliance.drop_duplicates(inplace=True)

# 4. Confirm dataset shape after cleaning
print("Data shape after cleaning:", df_reliance.shape)

# 5. Preview cleaned data
print(df_reliance.head())
