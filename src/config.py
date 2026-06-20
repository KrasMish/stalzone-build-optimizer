from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict

DEFAULT_VALIDATION_LIMITS: Dict[str, float] = {
    'radiation': -0.5,
    'temperature': -0.5,
    'biological_infection': -0.5,
    'psi': -0.5,
    'cold': 1.0,
}

DEFAULT_PARAMETER_WEIGHTS: Dict[str, int] = {
    'effective_health': 10,
    'bullet_resistance': 10,
    'vitality': 10,
    'healing_efficiency': 9,
    'health_regeneration': 9,
    'movement_speed': 8,
    'carry_weight': 6,
    'stamina_recovery': 5,
    'bleeding_protection': 5,
    'rupture_protection': 5,
    'explosion_protection': 3,
    'fire_protection': 3,
    'electro_protection': 3,
    'chemical_protection': 3,
    'radiation_protection': 3,
    'temperature_protection': 3,
    'bio_protection': 3,
    'psi_protection': 3,
    'healing_per_second': 1,
    'stamina': 1,
    'burn_reaction': 1,
    'rupture_reaction': 1,
    'radiation': 1,
    'temperature': 1,
    'biological_infection': 1,
    'psi': 1,
    'cold': 1,
}


@dataclass(frozen=True)
class BuildValidationConfig:
    limits: Dict[str, float] = field(default_factory=lambda: DEFAULT_VALIDATION_LIMITS.copy())


@dataclass(frozen=True)
class OptimizationConfig:
    parameter_weights: Dict[str, int] = field(default_factory=lambda: DEFAULT_PARAMETER_WEIGHTS.copy())


@dataclass(frozen=True)
class AppConfig:
    data_root: Path = Path('data')
    market_region: str = 'RU'
    budget: int = 0
    stalcraftdb_base_url: str = 'https://stalcraftdb.net'
    validation: BuildValidationConfig = field(default_factory=BuildValidationConfig)
    optimization: OptimizationConfig = field(default_factory=OptimizationConfig)
