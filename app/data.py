import yfinance as yf
import pandas as pd

def fetch_ohlc(symbol: str, period: str = "90d", interval: str = "1h") -> pd.DataFrame:
    df = yf.Ticker(symbol).history(period=period, interval=interval, auto_adjust=False)
    df = df.rename(columns=str.lower)
    return df.dropna()
