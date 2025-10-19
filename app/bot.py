import json
from datetime import datetime, timezone
from .config import CONFIG
from .data import fetch_ohlc
from .strategy import sma_crossover_signals
from .broker_alpaca import AlpacaBroker
from .notify import send as notify
from .broker_stub import StubBroker

def _now():
    return datetime.now(timezone.utc).isoformat()

def evaluate_symbol(symbol: str, broker):
    candles = fetch_ohlc(symbol, period="90d", interval=CONFIG['TIMEFRAME'])
    if candles.empty or len(candles) < max(CONFIG['FAST_WINDOW'], CONFIG['SLOW_WINDOW']) + 2:
        return {"symbol": symbol, "status": "insufficient_data"}

    sig = sma_crossover_signals(candles, CONFIG['FAST_WINDOW'], CONFIG['SLOW_WINDOW'])
    last = sig.iloc[-1]
    price = float(last['close'])

    pos = None if CONFIG.get('DRY_RUN') else broker.get_position(symbol)
    current_exposure = 0.0 if not pos else abs(float(pos.get('market_value', 0)))
    can_add = current_exposure < CONFIG['MAX_POSITION_USD']

    action = "hold"
    details = {"price": price, "have_position": pos is not None, "current_exposure": current_exposure}

    if last['buy'] and can_add:
        order = broker.submit_order_market_notional(symbol, "buy", CONFIG['MAX_NOTIONAL_PER_SYMBOL'])
        action = "buy"
        details["order"] = order
    elif last['sell'] and (pos is not None or CONFIG.get('DRY_RUN')):
        broker.close_position(symbol)
        action = "sell_close"

    return {"symbol": symbol, "status": "ok", "action": action, "details": details}

def handler(event=None, context=None):
    broker = StubBroker() if CONFIG.get('DRY_RUN') else AlpacaBroker(CONFIG['ALPACA_BASE_URL'], CONFIG['ALPACA_KEY_ID'], CONFIG['ALPACA_SECRET_KEY'])
    out = {"ts": _now(), "symbols": []}
    for sym in CONFIG['SYMBOLS']:
        try:
            res = evaluate_symbol(sym, broker)
        except Exception as e:
            res = {"symbol": sym, "status": "error", "error": str(e)}
        out["symbols"].append(res)
    # compact log
    print(json.dumps(out, separators=(",", ":")))
    try:
        lines = [f"{s['symbol']}: {s.get('action','-')} {s.get('status','')}" for s in out['symbols']]
        notify("\n".join(lines))
    except Exception:
        pass
    return out
