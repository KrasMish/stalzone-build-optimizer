import unittest

from src.calculator.artifact_scaling import ArtifactSlotState, StatRange, calculate_artifact_stat
from src.calculator.formulas import FormulaEngine
from src.market.rarity import quality_to_rarity
from src.parser.price_parser import PriceParser


class FormulaTests(unittest.TestCase):
    def test_effective_health_formula(self) -> None:
        engine = FormulaEngine()
        stats = engine.calculate_derived_stats(
            {
                'bullet_resistance': 50.0,
                'vitality': 20.0,
            }
        )
        self.assertAlmostEqual(stats['effective_health'], 180.0)

    def test_container_protection_reduces_infection(self) -> None:
        engine = FormulaEngine()
        adjusted = engine.apply_container_protection({'radiation': 2.0}, protection=50.0)
        self.assertAlmostEqual(adjusted['radiation'], 1.0)

    def test_upgrade_bonus_applies_to_positive_stats(self) -> None:
        slot = ArtifactSlotState(quality=100.0, upgrade_level=15)
        stat_range = StatRange(min=10.0, max=10.0)
        value = calculate_artifact_stat(slot, 'Bullet resistance', stat_range)
        self.assertAlmostEqual(value, 13.0)


class PriceParserTests(unittest.TestCase):
    def test_groups_sales_by_rarity_and_averages_last_week(self) -> None:
        parser = PriceParser()
        payload = {
            'artifacts': {
                'abc': {
                    'sales': [
                        {'quality': 137, 'upgrade': 15, 'price': 3_000_000, 'sold_at': '2026-06-19T12:00:00+00:00'},
                        {'quality': 132, 'upgrade': 15, 'price': 3_500_000, 'sold_at': '2026-06-18T12:00:00+00:00'},
                        {'quality': 110, 'upgrade': 15, 'price': 900_000, 'sold_at': '2026-06-17T12:00:00+00:00'},
                    ]
                }
            }
        }

        records = parser.parse_price_feed(payload, 'RU')
        prices = {(record.artifact_id, record.rarity): record.price for record in records}

        self.assertEqual(quality_to_rarity(137), 'rare')
        self.assertEqual(prices[('abc', 'rare')], 3_250_000)
        self.assertEqual(prices[('abc', 'uncommon')], 900_000)

    def test_ignores_non_plus_fifteen_sales(self) -> None:
        parser = PriceParser()
        payload = {
            'artifacts': {
                'abc': {
                    'sales': [
                        {'quality': 130, 'upgrade': 10, 'price': 100, 'sold_at': '2026-06-19T12:00:00+00:00'},
                    ]
                }
            }
        }
        self.assertEqual(parser.parse_price_feed(payload, 'RU'), [])


if __name__ == '__main__':
    unittest.main()
