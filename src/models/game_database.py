from dataclasses import dataclass
from typing import Dict

from src.models.armor import ArmorDefinition
from src.models.artifact import ArtifactDefinition
from src.models.container import ContainerDefinition


@dataclass
class GameDatabase:
    artifacts: Dict[str, ArtifactDefinition]
    armors: Dict[str, ArmorDefinition]
    containers: Dict[str, ContainerDefinition]
