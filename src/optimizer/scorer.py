from typing import Dict


class ScoreCalculator:
    def __init__(self, weights: Dict[str, int]) -> None:
        self.weights = weights

    def score(self, stats: Dict[str, float]) -> float:
        return sum(stats.get(name, 0.0) * weight for name, weight in self.weights.items())
