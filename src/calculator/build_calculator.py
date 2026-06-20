from typing import Dict, Iterable

from src.calculator.artifact_scaling import StatRange
from src.calculator.formulas import FormulaEngine
from src.calculator.stat_keys import stat_key
from src.models.armor import Armor
from src.models.artifact import Artifact, ArtifactDefinition
from src.models.container import Container
from src.models.game_database import GameDatabase


class BuildCalculator:
    def __init__(self, formulas: FormulaEngine, database: GameDatabase) -> None:
        self.formulas = formulas
        self.database = database

    def calculate_build_stats(
        self,
        armor: Armor | None,
        container: Container | None,
        artifacts: Iterable[Artifact],
    ) -> Dict[str, float]:
        totals: Dict[str, float] = {}
        container_def = self.database.containers.get(container.id) if container else None
        protection = container.protection if container else 0.0
        efficiency = container.efficiency if container else 100.0

        for artifact in artifacts:
            definition = self.database.artifacts.get(artifact.id)
            if definition is None:
                for key, value in artifact.stats.items():
                    totals[key] = totals.get(key, 0.0) + value
                continue

            stat_ranges = {
                name: StatRange(data.min, data.max)
                for name, data in definition.stat_ranges.items()
            }
            additional_ranges = self._resolve_additional_stats(definition, artifact)
            contribution = self.formulas.calculate_artifact_contribution(
                artifact,
                stat_ranges,
                additional_ranges,
                container_efficiency=efficiency,
            )
            for key, value in contribution.items():
                totals[key] = totals.get(key, 0.0) + value

        totals = self.formulas.apply_container_protection(totals, protection)

        if container_def is not None:
            for key, value in container_def.stats.items():
                totals[key] = totals.get(key, 0.0) + value

        if armor is not None:
            armor_def = self.database.armors.get(armor.id)
            if armor_def is not None:
                for display_name, value in armor_def.stats.items():
                    key = stat_key(display_name)
                    totals[key] = totals.get(key, 0.0) + value

        return self.formulas.calculate_derived_stats(totals)

    def _resolve_additional_stats(
        self,
        definition: ArtifactDefinition,
        artifact: Artifact,
    ) -> Dict[str, StatRange]:
        additional_ranges: Dict[str, StatRange] = {}
        selected_ids = [prop_id for prop_id in artifact.additional_property_ids if prop_id]

        for additional in definition.additional_stats:
            if selected_ids and additional.stat_id not in selected_ids:
                continue
            if not selected_ids:
                continue
            additional_ranges[additional.name_en] = StatRange(
                additional.value.min,
                additional.value.max,
            )

        return additional_ranges
