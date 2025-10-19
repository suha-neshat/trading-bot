import os

def get_env_float(key, default):
    try:
        return float(os.getenv(key, default))
    except Exception:
        return float(default)

CONFIG = {
    "ALPACA_BASE_URL": os.getenv("ALPACA_BASE_URL", "https://paper-api.alpaca.markets"),
    "ALPACA_KEY_ID": os.getenv("ALPACA_KEY_ID", ""),
    "ALPACA_SECRET_KEY": os.getenv("ALPACA_SECRET_KEY", ""),
    "SYMBOLS": [s.strip().upper() for s in os.getenv("SYMBOLS", "AAPL,MSFT").split(",") if s.strip()],
    "TIMEFRAME": os.getenv("TIMEFRAME", "1h"),
    "FAST_WINDOW": int(os.getenv("FAST_WINDOW", "20")),
    "SLOW_WINDOW": int(os.getenv("SLOW_WINDOW", "50")),
    "MAX_NOTIONAL_PER_SYMBOL": get_env_float("MAX_NOTIONAL_PER_SYMBOL", 500),
    "MAX_POSITION_USD": get_env_float("MAX_POSITION_USD", 1000),
    "STOP_LOSS_PCT": get_env_float("STOP_LOSS_PCT", 0.03),
    "TAKE_PROFIT_PCT": get_env_float("TAKE_PROFIT_PCT", 0.06),
}
CONFIG['DRY_RUN'] = os.getenv('DRY_RUN', 'true').lower() in ('1','true','yes','y')
