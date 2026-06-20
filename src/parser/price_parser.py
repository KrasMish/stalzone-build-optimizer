from datetime import datetime, timedelta, timezone
from typing import Any

from src.market.rarity import quality_to_rarity
from src.models.price import PriceRecord


class PriceParser:
    def parse_price_feed(self, payload: Any, region: str) -> list[PriceRecord]:
        if not isinstance(payload, dict):
            raise ValueError('Price feed payload must be a JSON object.')

        artifacts = payload.get('artifacts', payload)
        if not isinstance(artifacts, dict):
            raise ValueError('Price feed must contain an "artifacts" object.')

        records: list[PriceRecord] = []
        now = datetime.now(timezone.utc)
        week_ago = now - timedelta(days=7)

        for artifact_id, artifact_data in artifacts.items():
            if not isinstance(artifact_data, dict):
                continue

            sales = artifact_data.get('sales', [])
            if not isinstance(sales, list):
                continue

            grouped: dict[str, list[int]] = {}
            latest: dict[str, tuple[int, datetime]] = {}

            for sale in sales:
                if not isinstance(sale, dict):
                    continue
                if int(sale.get('upgrade', 15)) != 15:
                    continue

                quality = float(sale.get('quality', 0))
                price = int(sale.get('price', 0))
                if price <= 0 or quality <= 0:
                    continue

                rarity = quality_to_rarity(quality)
                if rarity == 'unknown':
                    continue

                sold_at = self._parse_datetime(sale.get('sold_at'))
                if sold_at is not None and sold_at >= week_ago:
                    grouped.setdefault(rarity, []).append(price)

                if sold_at is None:
                    continue

                current_latest = latest.get(rarity)
                if current_latest is None or sold_at > current_latest[1]:
                    latest[rarity] = (price, sold_at)

            for rarity in {'common', 'uncommon', 'special', 'rare', 'epic', 'legendary'}:
                if rarity in grouped:
                    average_price = sum(grouped[rarity]) // len(grouped[rarity])
                elif rarity in latest:
                    average_price = latest[rarity][0]
                else:
                    continue

                records.append(
                    PriceRecord(
                        artifact_id=str(artifact_id),
                        rarity=rarity,
                        price=average_price,
                        region=region.upper(),
                    )
                )

        return records

    @staticmethod
    def _parse_datetime(value: Any) -> datetime | None:
        if value is None:
            return None
        if isinstance(value, (int, float)):
            return datetime.fromtimestamp(value, tz=timezone.utc)
        if isinstance(value, str):
            normalized = value.replace('Z', '+00:00')
            return datetime.fromisoformat(normalized)
        return None
