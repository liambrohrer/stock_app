import requests

API_key = "2CSPURIKMG8JEO5W"

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
print(data)
