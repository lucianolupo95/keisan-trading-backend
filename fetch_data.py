import argparse
from src.data.fetcher import fetch_and_save

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch stock data")
    parser.add_argument("symbol", help="Ticker symbol (e.g., AAPL)")
    parser.add_argument("--start", help="Start date (YYYY-MM-DD)", default=None)
    parser.add_argument("--end", help="End date (YYYY-MM-DD)", default=None)
    parser.add_argument("--interval", help="Interval (1d, 1h, 1m...)", default="1d")

    args = parser.parse_args()
    fetch_and_save(args.symbol, args.start, args.end, args.interval)
