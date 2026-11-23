from pathlib import Path
import json

import pandas as pd


STOCK_NAMES = {
    "AAPL": "Apple",
    "MSFT": "Microsoft",
    "NVDA": "NVIDIA",
}

DATA_DIR = Path(__file__).resolve().parent
CSV_FILES = sorted(DATA_DIR.glob("*_daily_prices.csv"))
OUTPUT_FILE = DATA_DIR / "latest_stock_data.json"


def main():
    if not CSV_FILES:
        print(f"No *_daily_prices.csv files found in {DATA_DIR}")
        return

    observations = []

    for csv_file in CSV_FILES:
        symbol = csv_file.name.removesuffix("_daily_prices.csv")
        stock_name = STOCK_NAMES.get(symbol, symbol)

        try:
            df = pd.read_csv(csv_file, parse_dates=["date"])
        except (ValueError, OSError) as error:
            print(f"Skipping {csv_file.name}: {error}")
            continue

        if df.empty:
            print(f"Skipping {csv_file.name}: file has no observations")
            continue

        latest = df.sort_values("date").iloc[-1]
        observation = {
            "Stock": stock_name,
            "Symbol": symbol,
            "Date": latest["date"].date().isoformat(),
        }
        for column in ("open", "high", "low", "close", "volume"):
            if column in df.columns:
                value = latest[column]
                observation[column] = int(value) if column == "volume" else float(value)
        observations.append(observation)

    if observations:
        OUTPUT_FILE.write_text(json.dumps(observations, indent=2) + "\n", encoding="utf-8")
        print(f"Saved latest observations to {OUTPUT_FILE}")
    else:
        print("No valid stock observations found.")


if __name__ == "__main__":
    main()
