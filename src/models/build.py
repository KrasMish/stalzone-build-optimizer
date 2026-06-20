from dataclasses import dataclass, field
from typing import Dict, List
from src.models.armor import Armor
from src.models.artifact import Artifact
from src.models.container import Container


@dataclass
class Build:
    armor: Armor | None
    container: Container | None
    artifacts: List[Artifact]
    total_price: int = 0
    stats: Dict[str, float] = field(default_factory=dict)
    score: float = 0.0
