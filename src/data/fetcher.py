import yfinance as yf
import pandas as pd
from config.db import get_engine

def fetch_and_save(symbol, start=None, end=None, interval="1d"):
    if interval in ["1m", "2m", "5m", "15m", "30m", "60m", "90m"]:
        # para datos intradía solo se permite usar "period"
        data = yf.download(symbol, period="7d", interval=interval)
    else:
        data = yf.download(symbol, start=start, end=end, interval=interval)

    if data.empty:
        print(f"No data found for {symbol}")
        return

    data.reset_index(inplace=True)
    data["symbol"] = symbol

    engine = get_engine()
    data.to_sql("stock_prices", engine, if_exists="append", index=False)

    print(f"Saved {len(data)} rows of data for {symbol} (interval={interval})")
