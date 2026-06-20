from dataclasses import dataclass, field
from typing import Dict


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
class Container:
    id: str
    name: str
    protection: float = 0.0
    efficiency: float = 100.0
    stats: Dict[str, float] = field(default_factory=dict)
