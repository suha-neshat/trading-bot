class StubBroker:
    """A broker drop-in that logs actions instead of sending real orders."""
    def __init__(self): pass
    def get_account(self):
        return {"status": "DRY_RUN", "cash": "100000"}
    def get_position(self, symbol: str):
        return None
    def submit_order_market_notional(self, symbol: str, side: str, notional_usd: float):
        return {"symbol": symbol, "side": side, "notional": round(float(notional_usd),2), "status": "SIMULATED"}
    def close_position(self, symbol: str, side: str = "sell"):
        return True
