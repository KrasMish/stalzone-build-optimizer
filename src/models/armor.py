from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class ArmorDefinition:
    id: str
    name: str
    name_ru: str
    stats: Dict[str, float]


@dataclass(frozen=True)
class Armor:
    id: str
    name: str
    stats: Dict[str, float]
    upgrade_level: int = 0
