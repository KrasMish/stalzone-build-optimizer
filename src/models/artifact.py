from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


@dataclass(frozen=True)
class StatRangeData:
    min: float
    max: float


@dataclass(frozen=True)
class AdditionalStatDefinition:
    stat_id: str
    name_en: str
    name_ru: str
    value: StatRangeData


@dataclass(frozen=True)
class ArtifactDefinition:
    id: str
    name: str
    name_ru: str
    stat_ranges: Dict[str, StatRangeData]
    additional_stats: Tuple[AdditionalStatDefinition, ...] = ()


@dataclass(frozen=True)
class ArmorDefinition:
    id: str
    name: str
    name_ru: str
    stats: Dict[str, float]


@dataclass(frozen=True)
class ContainerDefinition:
    id: str
    name: str
    name_ru: str
    protection: float
    efficiency: float
    capacity: int
    stats: Dict[str, float]


@dataclass(frozen=True)
class Artifact:
    id: str
    name: str
    rarity: str
    quality: float
    upgrade_level: int = 15
    additional_property_ids: Tuple[Optional[str], ...] = (None, None, None)
    stats: Dict[str, float] = field(default_factory=dict)
    price: int = 0

    @property
    def has_unknown_price(self) -> bool:
        return self.price <= 0
