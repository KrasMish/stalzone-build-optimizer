from src.config import DEFAULT_PARAMETER_WEIGHTS


PLAYSTYLE_PRESETS: dict[str, dict[str, int]] = {
    'tank': {
        'effective_health': 10,
        'vitality': 10,
        'bullet_resistance': 10,
        'healing_efficiency': 9,
        'carry_weight': 5,
        'movement_speed': 3,
    },
    'speed': {
        'movement_speed': 10,
        'stamina_recovery': 8,
        'carry_weight': 6,
        'effective_health': 5,
        'bullet_resistance': 5,
    },
    'hybrid': {
        'effective_health': 8,
        'bullet_resistance': 8,
        'movement_speed': 7,
        'carry_weight': 6,
        'vitality': 6,
    },
    'carry': {
        'carry_weight': 10,
        'vitality': 8,
        'bullet_resistance': 8,
    },
}


def parse_priority_overrides(raw: str | None) -> dict[str, int]:
    if not raw:
        return {}

    overrides: dict[str, int] = {}
    for chunk in raw.split(','):
        if ':' not in chunk:
            continue
        key, value = chunk.split(':', 1)
        overrides[key.strip()] = int(value.strip())
    return overrides


def resolve_weights(playstyle: str | None, priority_override: str | None) -> dict[str, int]:
    weights = DEFAULT_PARAMETER_WEIGHTS.copy()

    if playstyle:
        preset = PLAYSTYLE_PRESETS.get(playstyle.lower())
        if preset:
            weights.update(preset)

    weights.update(parse_priority_overrides(priority_override))
    return weights
