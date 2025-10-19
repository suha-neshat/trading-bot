import requests
from typing import Dict, Any, Optional

class AlpacaBroker:
    def __init__(self, base_url: str, key_id: str, secret_key: str):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            "APCA-API-KEY-ID": key_id,
            "APCA-API-SECRET-KEY": secret_key,
            "Content-Type": "application/json"
        })

    def get_account(self) -> Dict[str, Any]:
        r = self.session.get(f"{self.base_url}/v2/account")
        r.raise_for_status()
        return r.json()

    def get_position(self, symbol: str) -> Optional[Dict[str, Any]]:
        r = self.session.get(f"{self.base_url}/v2/positions/{symbol}")
        if r.status_code == 404:
            return None
        r.raise_for_status()
        return r.json()

    def submit_order_market_notional(self, symbol: str, side: str, notional_usd: float):
        payload = {"symbol": symbol, "side": side, "type": "market", "time_in_force": "gtc", "notional": str(round(notional_usd, 2))}
        r = self.session.post(f"{self.base_url}/v2/orders", json=payload)
        r.raise_for_status()
        return r.json()

    def close_position(self, symbol: str, side: str = "sell"):
        r = self.session.delete(f"{self.base_url}/v2/positions/{symbol}", params={"position_qty": "all"})
        if r.status_code not in (200, 204):
            r.raise_for_status()
        return True
