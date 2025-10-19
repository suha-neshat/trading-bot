import os, time
from datetime import datetime
os.environ.setdefault('DRY_RUN', 'true')

from app.config import CONFIG
from app.data import fetch_ohlc
from app.strategy import sma_crossover_signals
from app.broker_stub import StubBroker

def step(symbol, broker):
    df = fetch_ohlc(symbol, period='30d', interval=CONFIG['TIMEFRAME'])
    if df.empty:
        print(f"{datetime.now().isoformat()} | {symbol} | no data"); return
    sig = sma_crossover_signals(df, CONFIG['FAST_WINDOW'], CONFIG['SLOW_WINDOW'])
    last = sig.iloc[-1]
    action = 'hold'
    if last['buy']:
        broker.submit_order_market_notional(symbol, 'buy', CONFIG['MAX_NOTIONAL_PER_SYMBOL'])
        action = 'buy'
    elif last['sell']:
        broker.close_position(symbol)
        action = 'sell_close'
    print(f"{datetime.now().isoformat()} | {symbol:<6} | {action:<10} | close={float(last['close']):.2f}")

if __name__ == '__main__':
    broker = StubBroker()
    print('DRY_RUN live loop started. Press Ctrl+C to stop. Symbols:', CONFIG['SYMBOLS'])
    while True:
        for s in CONFIG['SYMBOLS']:
            try:
                step(s, broker)
            except Exception as e:
                print('error', s, e)
        time.sleep(60)
