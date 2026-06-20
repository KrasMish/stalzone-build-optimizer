from typing import Optional

from src.models.build import Build


class Advisor:
    def explain(self, build: Build, reference_build: Optional[Build] = None) -> str:
        if reference_build is None:
            return (
                f'This build is the top-ranked candidate with score {build.score:.1f} '
                f'and total price {build.total_price:,}.'
            )

        score_delta = build.score - reference_build.score
        effective_health = build.stats.get('effective_health', 0.0)
        reference_effective_health = reference_build.stats.get('effective_health', 0.0)

        if reference_effective_health > 0:
            effective_health_delta = (
                (effective_health - reference_effective_health) / reference_effective_health
            ) * 100.0
            return (
                f'This build scores {build.score:.1f}, which is {score_delta:.1f} points higher than the '
                f'reference build, with {effective_health_delta:.1f}% more Effective Health while staying '
                f'within the configured budget.'
            )

        return (
            f'This build scores {build.score:.1f}, which is {score_delta:.1f} points higher than the '
            f'reference build while remaining within the configured budget.'
        )
