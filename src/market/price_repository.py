from pathlib import Path
from typing import Dict

from src.models.price import PriceRecord
from src.utils.json_utils import load_json, save_json


class PriceRepository:
    def __init__(self, prices_root: Path) -> None:
        self.prices_root = prices_root
        self.prices_root.mkdir(parents=True, exist_ok=True)

    def region_path(self, region: str) -> Path:
        return self.prices_root / f'{region.lower()}.json'

    def load_region(self, region: str) -> Dict[str, Dict[str, int]]:
        path = self.region_path(region)
        if not path.exists() or path.stat().st_size == 0:
            return {}

        payload = load_json(path)
        if isinstance(payload, dict) and 'artifacts' in payload:
            return self._records_from_feed(payload, region)

        if isinstance(payload, dict):
            return payload

        return {}

    def save_region(self, region: str, records: list[PriceRecord]) -> None:
        grouped: Dict[str, Dict[str, int]] = {}
        for record in records:
            grouped.setdefault(record.artifact_id, {})[record.rarity] = record.price

        save_json(
            self.region_path(region),
            {
                'region': region.upper(),
                'artifacts': grouped,
            },
        )

    def get_price(self, region_prices: Dict[str, Dict[str, int]], artifact_id: str, rarity: str) -> int:
        artifact_prices = region_prices.get(artifact_id, {})
        return int(artifact_prices.get(rarity, 0))

    @staticmethod
    def _records_from_feed(payload: dict, region: str) -> Dict[str, Dict[str, int]]:
        artifacts = payload.get('artifacts', {})
        if not isinstance(artifacts, dict):
            return {}

        result: Dict[str, Dict[str, int]] = {}
        for artifact_id, prices in artifacts.items():
            if isinstance(prices, dict):
                result[str(artifact_id)] = {
                    str(rarity): int(price)
                    for rarity, price in prices.items()
                    if isinstance(price, (int, float))
                }
        return result
