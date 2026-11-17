import requests
import pandas as pd

response = requests.get(
    "https://www.alphavantage.co/query",
    params={
        "function": "TIME_SERIES_DAILY",
        "symbol": "IBM",
        "outputsize": "compact",
        "apikey": "YOUR_KEY",
    },
    timeout=30,
)
response.raise_for_status()
data = response.json()

# The time series is stored under a label such as "Time Series (Daily)".
series_name = next(
    (key for key in data if key.startswith("Time Series")),
    None,
)

if series_name is None:
    raise ValueError(f"API did not return time-series data: {data}")

# Turn the nested JSON into rows, then make dates and prices usable.
df = pd.DataFrame.from_dict(data[series_name], orient="index")
df.index.name = "date"
df = df.rename(columns={
    "1. open": "open",
    "2. high": "high",
    "3. low": "low",
    "4. close": "close",
    "5. volume": "volume",
})

# API values arrive as text; convert prices and volume to numbers.
df = df.astype(float)
df = df.sort_index()

df.to_csv("/Users/liamrohrer/Documents/Education/Personal_Projects/stock_app/IBM_daily_prices.csv")
print(df.head())