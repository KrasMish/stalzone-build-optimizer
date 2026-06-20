import heapq
import itertools
import time
from typing import Iterable, List

from src.calculator.build_calculator import BuildCalculator
from src.models.armor import Armor
from src.models.artifact import Artifact
from src.models.build import Build
from src.models.container import Container
from src.optimizer.filters import BuildValidator
from src.optimizer.scorer import ScoreCalculator
from src.utils.logger import get_logger

logger = get_logger(__name__)


class BuildOptimizer:
    def __init__(
        self,
        calculator: BuildCalculator,
        validator: BuildValidator,
        scorer: ScoreCalculator,
        artifact_slot_count: int = 6,
        max_candidates: int = 10000,
    ) -> None:
        self.calculator = calculator
        self.validator = validator
        self.scorer = scorer
        self.artifact_slot_count = artifact_slot_count
        self.max_candidates = max_candidates

    def optimize(
        self,
        artifacts: list[Artifact],
        armor: Armor | None,
        container: Container | None,
        budget: int,
        top_n: int = 10,
    ) -> List[Build]:
        started_at = time.perf_counter()
        top_builds: list[tuple[float, Build]] = []
        evaluated = 0

        for candidate in self._generate_candidates(artifacts):
            evaluated += 1
            total_price = sum(artifact.price for artifact in candidate)
            if budget and total_price > budget:
                continue
            if any(artifact.has_unknown_price for artifact in candidate):
                continue

            stats = self.calculator.calculate_build_stats(armor, container, candidate)
            build = Build(
                armor=armor,
                container=container,
                artifacts=list(candidate),
                total_price=total_price,
                stats=stats,
            )
            if not self.validator.is_valid(build):
                continue

            build.score = self.scorer.score(build.stats)
            if len(top_builds) < top_n:
                heapq.heappush(top_builds, (build.score, build))
            elif build.score > top_builds[0][0]:
                heapq.heapreplace(top_builds, (build.score, build))

        elapsed = time.perf_counter() - started_at
        logger.info('Evaluated %s candidates in %.3fs', evaluated, elapsed)

        ranked = sorted(top_builds, key=lambda item: item[0], reverse=True)
        return [build for _, build in ranked]

    def _generate_candidates(self, artifacts: list[Artifact]) -> Iterable[tuple[Artifact, ...]]:
        priced_artifacts = [artifact for artifact in artifacts if artifact.price > 0]
        if len(priced_artifacts) < self.artifact_slot_count:
            if priced_artifacts:
                yield tuple(priced_artifacts)
            return

        for count, candidate in enumerate(
            itertools.combinations(priced_artifacts, self.artifact_slot_count),
            start=1,
        ):
            if count > self.max_candidates:
                break
            yield candidate
