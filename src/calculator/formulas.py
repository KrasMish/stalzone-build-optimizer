from typing import Dict, Iterable, Mapping

from src.calculator.artifact_scaling import (
    ArtifactSlotState,
    StatRange,
    calculate_additional_stat,
    calculate_artifact_stat,
)
from src.calculator.constants import INFECTION_STAT_NAMES
from src.calculator.stat_keys import stat_key
from src.models.armor import Armor
from src.models.artifact import Artifact
from src.models.container import Container


class FormulaEngine:
    def aggregate_artifact_stats(self, artifacts: Iterable[Artifact]) -> Dict[str, float]:
        totals: Dict[str, float] = {}
        for artifact in artifacts:
            for key, value in artifact.stats.items():
                totals[key] = totals.get(key, 0.0) + value
        return totals

    def calculate_artifact_contribution(
        self,
        artifact: Artifact,
        stat_ranges: Mapping[str, StatRange],
        additional_ranges: Mapping[str, StatRange],
        container_efficiency: float = 100.0,
    ) -> Dict[str, float]:
        slot = ArtifactSlotState(quality=artifact.quality, upgrade_level=artifact.upgrade_level)
        totals: Dict[str, float] = {}

        for display_name, stat_range in stat_ranges.items():
            key = stat_key(display_name)
            value = calculate_artifact_stat(slot, display_name, stat_range)
            if container_efficiency != 100.0:
                value *= container_efficiency / 100.0
            totals[key] = totals.get(key, 0.0) + value

        for display_name, stat_range in additional_ranges.items():
            key = stat_key(display_name)
            value = calculate_additional_stat(slot, display_name, stat_range)
            if container_efficiency != 100.0:
                value *= container_efficiency / 100.0
            totals[key] = totals.get(key, 0.0) + value

        return totals

    def apply_container_protection(self, stats: Dict[str, float], protection: float) -> Dict[str, float]:
        if protection <= 0:
            return dict(stats)

        adjusted = dict(stats)
        for display_name in INFECTION_STAT_NAMES:
            key = stat_key(display_name)
            if key not in adjusted:
                continue
            value = adjusted[key]
            adjusted[key] = value - (value / 100.0) * protection
        return adjusted

    def calculate_derived_stats(self, base_stats: Dict[str, float]) -> Dict[str, float]:
        stats = dict(base_stats)
        bullet_resistance = stats.get('bullet_resistance', 0.0)
        vitality = stats.get('vitality', 0.0)
        stats['effective_health'] = ((100.0 + bullet_resistance) / 100.0) * (100.0 + vitality)
        return stats
