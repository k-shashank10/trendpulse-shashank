import requests
import json

# API endpoint and parameters
url = "https://www.alphavantage.co/query"
params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": "RELIANCE.BSE",
    "outputsize": "full",
    "apikey": "43HX4XDDDGSPIRJP"   
}

# Fetch data from API
response = requests.get(url, params=params)

# Check if request was successful
if response.status_code == 200:
    data = response.json()

    # Save to JSON file
    with open("reliance_daily.json", "w") as f:
        json.dump(data, f, indent=4)

    print("Data saved to reliance_daily.json")
else:
    print("Error fetching data:", response.status_code)
