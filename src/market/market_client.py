from typing import Any, Dict
import requests


class MarketClient:
    def __init__(self, base_url: str, timeout: int = 10) -> None:
        self.base_url = base_url
        self.timeout = timeout

    def fetch_price_data(self, endpoint: str) -> Dict[str, Any]:
        response = requests.get(f'{self.base_url}/{endpoint}', timeout=self.timeout)
        response.raise_for_status()
        return response.json()
