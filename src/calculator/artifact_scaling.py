from dataclasses import dataclass

from src.calculator.constants import NEGATIVE_STAT_NAMES


@dataclass(frozen=True)
class StatRange:
    min: float
    max: float


@dataclass(frozen=True)
class ArtifactSlotState:
    quality: float
    upgrade_level: int


def get_rarity_tier(quality: float) -> int:
    if quality <= 100:
        return 0
    if quality <= 109.9:
        return 1
    if quality <= 119.9:
        return 2
    if quality <= 129.9:
        return 3
    if quality <= 139.9:
        return 4
    if quality <= 149.9:
        return 5
    return 6


def calculate_artifact_stat(
    slot: ArtifactSlotState,
    stat_name: str,
    stat_range: StatRange,
) -> float:
    rarity_tier = get_rarity_tier(slot.quality)
    min_value = stat_range.min
    max_value = stat_range.max
    buff = min_value + (min_value / 100) * (slot.quality - 100)
    buff_by_min = min_value + (max_value / 100) * (slot.quality - 100)
    buff_by_max = max_value + (min_value / 100) * (slot.quality - 100)
    mind = max_value * 0.9
    extra_quality = slot.quality - (100 + 10 * rarity_tier)
    is_negative = stat_name in NEGATIVE_STAT_NAMES
    upgrade_bonus = slot.upgrade_level * 2

    if slot.quality <= 100:
        if is_negative:
            if max_value > 0:
                return buff_by_max + (buff_by_max / 100)
            return buff_by_min + (buff_by_min / 100) * upgrade_bonus

        if max_value > 0:
            return buff_by_max + (buff_by_max / 100) * upgrade_bonus
        return buff_by_min + (buff_by_min / 100)

    if is_negative:
        if max_value > 0:
            return max_value + ((max_value - mind) / 100) * (extra_quality * 10)
        return buff + (buff / 100) * upgrade_bonus

    if max_value > 0:
        base_value = max_value + (max_value / 100) * (slot.quality - 100)
        return base_value + (base_value / 100) * upgrade_bonus

    return min_value + ((max_value - mind) / 100) * (extra_quality * 20)


def calculate_additional_stat(
    slot: ArtifactSlotState,
    stat_name: str,
    stat_range: StatRange,
) -> float:
    min_value = stat_range.min
    max_value = stat_range.max
    min_buff = min_value + ((max_value - min_value) / 100) * slot.quality
    max_buff = max_value + (max_value / 100) * (slot.quality - 100)
    negative_buff = min_value + (min_value / 100) * (slot.quality - 100)
    is_negative = stat_name in NEGATIVE_STAT_NAMES
    upgrade_bonus = slot.upgrade_level * 2

    if slot.quality >= 100:
        if is_negative and max_value < 0:
            return negative_buff + (negative_buff / 100) * upgrade_bonus
        return max_buff + (max_buff / 100) * upgrade_bonus

    return min_buff + (min_buff / 100) * upgrade_bonus
