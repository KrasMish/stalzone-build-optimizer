from pathlib import Path

from src.market.market_client import MarketClient
from src.market.price_repository import PriceRepository
from src.parser.price_parser import PriceParser
from src.utils.logger import get_logger

logger = get_logger(__name__)


class PriceUpdater:
    def __init__(
        self,
        client: MarketClient,
        parser: PriceParser,
        repository: PriceRepository,
    ) -> None:
        self.client = client
        self.parser = parser
        self.repository = repository

    def update_prices(self, region: str, *, feed_path: str | None = None) -> Path:
        endpoint = feed_path or f'api/market/{region.lower()}/artifacts.json'
        payload = self.client.fetch_price_data(endpoint)
        records = self.parser.parse_price_feed(payload, region)
        self.repository.save_region(region, records)
        logger.info('Updated %s price records for region %s', len(records), region.upper())
        return self.repository.region_path(region)
