from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class QualityRarity:
    name: str
    min_quality: float
    max_quality: float | None = None


QUALITY_RARITIES: tuple[QualityRarity, ...] = (
    QualityRarity('common', 85, 99),
    QualityRarity('uncommon', 100, 114),
    QualityRarity('special', 115, 129),
    QualityRarity('rare', 130, 144),
    QualityRarity('epic', 145, 159),
    QualityRarity('legendary', 160, None),
)


def quality_to_rarity(quality: float) -> str:
    for rarity in QUALITY_RARITIES:
        if rarity.max_quality is None and quality >= rarity.min_quality:
            return rarity.name
        if rarity.max_quality is not None and rarity.min_quality <= quality <= rarity.max_quality:
            return rarity.name
    return 'unknown'
