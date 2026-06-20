from dataclasses import dataclass


@dataclass(frozen=True)
class PriceRecord:
    artifact_id: str
    rarity: str
    price: int
    region: str = 'RU'
