import argparse
from pathlib import Path

from src.ai.advisor import Advisor
from src.calculator.build_calculator import BuildCalculator
from src.calculator.formulas import FormulaEngine
from src.config import AppConfig
from src.market.price_repository import PriceRepository
from src.optimizer.filters import BuildValidator
from src.optimizer.optimizer import BuildOptimizer
from src.optimizer.priorities import resolve_weights
from src.optimizer.scorer import ScoreCalculator
from src.services.data_loader import DataLoader
from src.utils.logger import get_logger

logger = get_logger(__name__)


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='StalZone Build Optimizer')
    parser.add_argument('--region', default='RU', help='Market region (RU or EU)')
    parser.add_argument('--budget', type=int, default=0, help='Budget cap for build price')
    parser.add_argument('--top-n', type=int, default=5, help='Number of candidate builds to return')
    parser.add_argument('--armor', help='Armor item id from EXBO database')
    parser.add_argument('--container', help='Container item id from EXBO database')
    parser.add_argument('--quality', type=float, default=130.0, help='Default artifact quality percentage')
    parser.add_argument('--playstyle', choices=['tank', 'speed', 'hybrid', 'carry'], help='Optimization preset')
    parser.add_argument('--priority', help='Override weights, e.g. carry_weight:10,vitality:8')
    parser.add_argument('--sync-db', action='store_true', help='Refresh EXBO database cache')
    parser.add_argument('--max-candidates', type=int, default=10000, help='Maximum generated build combinations')
    return parser


def main() -> None:
    args = build_arg_parser().parse_args()
    config = AppConfig(data_root=Path('data'), market_region=args.region, budget=args.budget)
    loader = DataLoader(config.data_root)

    if args.sync_db:
        loader.sync_database()

    database = loader.load_database()
    price_repository = PriceRepository(config.data_root / 'prices')
    region_prices = price_repository.load_region(config.market_region)

    armor = loader.resolve_armor(database, args.armor)
    container = loader.resolve_container(database, args.container)
    artifacts = loader.build_artifact_catalog(
        database,
        region_prices,
        default_quality=args.quality,
    )

    weights = resolve_weights(args.playstyle, args.priority)
    formula_engine = FormulaEngine()
    calculator = BuildCalculator(formula_engine, database)
    validator = BuildValidator(config.validation)
    scorer = ScoreCalculator(weights)
    optimizer = BuildOptimizer(
        calculator,
        validator,
        scorer,
        max_candidates=args.max_candidates,
    )
    advisor = Advisor()

    logger.info(
        'Optimizing for region=%s budget=%s artifacts_with_prices=%s',
        args.region,
        args.budget,
        sum(1 for artifact in artifacts if artifact.price > 0),
    )

    builds = optimizer.optimize(artifacts, armor, container, args.budget, top_n=args.top_n)
    if not builds:
        logger.info(
            'No valid builds found. Sync database with --sync-db and populate data/prices/%s.json.',
            args.region.lower(),
        )
        return

    reference = builds[1] if len(builds) > 1 else None
    for index, build in enumerate(builds, start=1):
        logger.info(
            'Candidate #%s score=%.2f price=%s effective_health=%.2f',
            index,
            build.score,
            f'{build.total_price:,}',
            build.stats.get('effective_health', 0.0),
        )
        if index == 1:
            logger.info('Advisor: %s', advisor.explain(build, reference))


if __name__ == '__main__':
    main()
