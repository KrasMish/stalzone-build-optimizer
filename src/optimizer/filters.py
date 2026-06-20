from src.config import BuildValidationConfig
from src.models.build import Build


class BuildValidator:
    def __init__(self, config: BuildValidationConfig) -> None:
        self.config = config

    def is_valid(self, build: Build) -> bool:
        for stat, minimum in self.config.limits.items():
            if build.stats.get(stat, 0.0) < minimum:
                return False
        return True
