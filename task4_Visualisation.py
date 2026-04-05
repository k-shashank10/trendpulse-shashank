import json, pandas as pd, matplotlib.pyplot as plt

# Load JSON
with open("reliance_daily.json") as f:
    data = json.load(f)

# DataFrame
ts = data.get("Time Series (Daily)", {})
df = pd.DataFrame.from_dict(ts, orient="index")
df.columns = ["open","high","low","close","vol"]
df.index = pd.to_datetime(df.index)
df = df.astype(float).sort_index()

# Indicators
df["ret"] = df["close"].pct_change()
df["ma20"] = df["close"].rolling(20).mean()
df["ma50"] = df["close"].rolling(50).mean()
df["vol20"] = df["ret"].rolling(20).std()

delta = df["close"].diff()
gain = delta.where(delta>0,0).rolling(14).mean()
loss = (-delta.where(delta<0,0)).rolling(14).mean()
df["rsi"] = 100 - (100/(1+gain/loss))

# --- Plots ---
plt.figure(figsize=(12,8))

plt.subplot(3,1,1)
plt.plot(df.index, df["close"], label="Close", c="blue")
plt.plot(df.index, df["ma20"], label="MA20", c="orange")
plt.plot(df.index, df["ma50"], label="MA50", c="green")
plt.legend(); plt.title("Close + MA")

plt.subplot(3,1,2)
plt.plot(df.index, df["vol20"], c="red")
plt.title("Volatility (20d)")

plt.subplot(3,1,3)
plt.plot(df.index, df["rsi"], c="purple")
plt.axhline(70, ls="--", c="grey"); plt.axhline(30, ls="--", c="grey")
plt.title("RSI (14d)")

plt.tight_layout(); plt.show()
