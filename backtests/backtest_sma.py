import os
from app.data import fetch_ohlc
from app.strategy import sma_crossover_signals

SYMBOLS = [s.strip().upper() for s in os.getenv("SYMBOLS", "AAPL,MSFT").split(",")]
FAST = int(os.getenv("FAST_WINDOW", 20))
SLOW = int(os.getenv("SLOW_WINDOW", 50))
TIMEFRAME = os.getenv("TIMEFRAME", "1h")

def backtest(symbol: str):
    df = fetch_ohlc(symbol, period="365d", interval=TIMEFRAME)
    sig = sma_crossover_signals(df, FAST, SLOW)
    pos, cash, last_price = 0, 0.0, None
    for _, row in sig.iterrows():
        price = row['close']
        if row['buy'] and pos == 0:
            pos, last_price = 1, price
        elif row['sell'] and pos == 1:
            cash += price - last_price
            pos, last_price = 0, None
    return cash

if __name__ == "__main__":
    for s in SYMBOLS:
        pnl = backtest(s)
        print(f"{s:<6}: PnL (per-share basis) = ${pnl:.2f}")
