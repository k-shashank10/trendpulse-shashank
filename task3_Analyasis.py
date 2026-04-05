import json
import pandas as pd

# Load JSON
with open("reliance_daily.json", "r") as f:
    data = json.load(f)

# Convert to DataFrame
ts = data.get("Time Series (Daily)", {})
df = pd.DataFrame.from_dict(ts, orient="index")
df.columns = ["open", "high", "low", "close", "volume"]
df.index = pd.to_datetime(df.index)
df = df.astype({"open": float, "high": float, "low": float,
                "close": float, "volume": int})
df.sort_index(inplace=True)

# Indicators
df["ret"] = df["close"].pct_change()
df["ma20"] = df["close"].rolling(20).mean()
df["ma50"] = df["close"].rolling(50).mean()
df["vol"] = df["ret"].rolling(20).std()

delta = df["close"].diff()
gain = delta.where(delta > 0, 0).rolling(14).mean()
loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
rs = gain / loss
df["rsi"] = 100 - (100 / (1 + rs))

# Latest summary
last = df.iloc[-1]
trend = "Bullish" if last["ma20"] > last["ma50"] else "Bearish"
status = "Overbought" if last["rsi"] > 70 else "Oversold" if last["rsi"] < 30 else "Neutral"

print("\nReliance Stock Analysis Summary")
print("--------------------------------")
print(f"Latest Close Price: {latest['close']:.2f}")
print(f"20-day MA: {latest['MA20']:.2f}")
print(f"50-day MA: {latest['MA50']:.2f}")
print(f"Trend: {trend}")
print(f"RSI: {last['rsi']:.2f} ({status})")
print(f"Volatality for 20 days: {last['vol']:.4f}")
print(f"Avg Return: {df['ret'].mean():.4f}")
print(f"Max Gain: {df['ret'].max():.4f}")
print(f"Max Loss: {df['ret'].min():.4f}")
