from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class CalculatorConstraints:
    validation_limits: Dict[str, float]
    parameter_weights: Dict[str, int]
