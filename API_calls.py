import requests
import pandas as pd
import time
import os

API_KEY = os.environ["ALPHA_VANTAGE_API_KEY"]
symbols = ["AAPL", "MSFT", "NVDA"]

for symbol in symbols:
    response = requests.get(
        "https://www.alphavantage.co/query",
        params={
            "function": "TIME_SERIES_DAILY",
            "symbol": symbol,
            "outputsize": "full",
            "apikey": API_KEY,
        },
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    time.sleep(6)  # Sleep for 6 seconds to respect API rate limits

    series_name = next(
        (key for key in data if key.startswith("Time Series")),
        None,
    )

    if series_name is None:
        print(f"No time-series data for {symbol}: {data}")
        continue

    df = pd.DataFrame.from_dict(data[series_name], orient="index")
    df.index.name = "date"
    df = df.rename(columns={
        "1. open": "open",
        "2. high": "high",
        "3. low": "low",
        "4. close": "close",
        "5. volume": "volume",
    })
    df = df.astype(float).sort_index()
    df = df.tail(365)

    filename = f"{symbol}_daily_prices.csv"
    df.to_csv(filename)
    print(f"Saved {filename}")
