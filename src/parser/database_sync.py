import logging
from typing import Any, Iterable

import requests

from src.calculator.constants import EXBO_DATABASE_RAW_URL
from src.utils.logger import get_logger

logger = get_logger(__name__)


class DatabaseSync:
    def __init__(self, base_url: str = EXBO_DATABASE_RAW_URL, timeout: int = 30) -> None:
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout

    def fetch_listing(self) -> list[dict[str, Any]]:
        response = requests.get(f'{self.base_url}/listing.json', timeout=self.timeout)
        response.raise_for_status()
        payload = response.json()
        if not isinstance(payload, list):
            raise ValueError('EXBO listing.json must be a list.')
        return payload

    def fetch_item(self, relative_path: str) -> dict[str, Any]:
        response = requests.get(f'{self.base_url}/{relative_path}', timeout=self.timeout)
        response.raise_for_status()
        payload = response.json()
        if not isinstance(payload, dict):
            raise ValueError(f'Item payload must be an object: {relative_path}')
        return payload

    def fetch_relevant_items(self) -> Iterable[dict[str, Any]]:
        listing = self.fetch_listing()
        paths: set[str] = set()

        for entry in listing:
            data_path = entry.get('data')
            if not isinstance(data_path, str):
                continue
            if 'armor/device' in data_path:
                continue
            if not any(token in data_path for token in ('armor/', 'artefact/', 'containers/')):
                continue
            paths.add(data_path)

        logger.info('Fetching %s EXBO item files', len(paths))
        for relative_path in sorted(paths):
            yield self.fetch_item(relative_path)
