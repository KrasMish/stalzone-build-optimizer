from pathlib import Path
from typing import Any

from src.models.armor import Armor, ArmorDefinition
from src.models.artifact import AdditionalStatDefinition, Artifact, ArtifactDefinition, StatRangeData
from src.models.container import Container, ContainerDefinition
from src.models.game_database import GameDatabase
from src.parser.database_parser import DatabaseParser
from src.parser.database_sync import DatabaseSync
from src.utils.json_utils import load_json, save_json
from src.utils.logger import get_logger

logger = get_logger(__name__)

ADDITIONAL_STATS_URL = (
    'https://raw.githubusercontent.com/SbokyZahodi/stalcraft-calculator/main/_db/additional_stats.json'
)


class DataLoader:
    def __init__(self, data_root: Path) -> None:
        self.data_root = data_root
        self.processed_root = data_root / 'processed'
        self.processed_root.mkdir(parents=True, exist_ok=True)

    def sync_database(self) -> GameDatabase:
        sync = DatabaseSync()
        additional_stats = self._fetch_additional_stats()
        items = list(sync.fetch_relevant_items())
        database = DatabaseParser().parse_items(items, additional_stats)
        self._save_database(database)
        logger.info(
            'Synced EXBO database: %s artifacts, %s armors, %s containers',
            len(database.artifacts),
            len(database.armors),
            len(database.containers),
        )
        return database

    def load_database(self) -> GameDatabase:
        artifacts_path = self.processed_root / 'artifacts.json'
        armors_path = self.processed_root / 'armors.json'
        containers_path = self.processed_root / 'containers.json'

        if not artifacts_path.exists() or not armors_path.exists() or not containers_path.exists():
            logger.info('Processed database cache missing, syncing from EXBO...')
            return self.sync_database()

        return GameDatabase(
            artifacts=self._load_artifact_definitions(artifacts_path),
            armors=self._load_armor_definitions(armors_path),
            containers=self._load_container_definitions(containers_path),
        )

    def resolve_armor(self, database: GameDatabase, armor_id: str | None) -> Armor | None:
        if not armor_id:
            return None
        definition = database.armors.get(armor_id)
        if definition is None:
            return None
        from src.calculator.stat_keys import stat_key

        return Armor(
            id=definition.id,
            name=definition.name,
            stats={stat_key(name): value for name, value in definition.stats.items()},
        )

    def resolve_container(self, database: GameDatabase, container_id: str | None) -> Container | None:
        if not container_id:
            return None
        definition = database.containers.get(container_id)
        if definition is None:
            return None
        return Container(
            id=definition.id,
            name=definition.name,
            protection=definition.protection,
            efficiency=definition.efficiency,
            stats=dict(definition.stats),
        )

    def build_artifact_catalog(
        self,
        database: GameDatabase,
        region_prices: dict[str, dict[str, int]],
        *,
        default_quality: float = 130.0,
        default_upgrade: int = 15,
    ) -> list[Artifact]:
        from src.market.rarity import quality_to_rarity

        catalog: list[Artifact] = []
        for definition in database.artifacts.values():
            rarity = quality_to_rarity(default_quality)
            price = region_prices.get(definition.id, {}).get(rarity, 0)
            catalog.append(
                Artifact(
                    id=definition.id,
                    name=definition.name,
                    rarity=rarity,
                    quality=default_quality,
                    upgrade_level=default_upgrade,
                    price=price,
                )
            )
        return catalog

    def _save_database(self, database: GameDatabase) -> None:
        save_json(self.processed_root / 'artifacts.json', self._serialize_artifacts(database.artifacts))
        save_json(self.processed_root / 'armors.json', self._serialize_armors(database.armors))
        save_json(self.processed_root / 'containers.json', self._serialize_containers(database.containers))

    @staticmethod
    def _fetch_additional_stats() -> list[dict[str, Any]]:
        import requests

        response = requests.get(ADDITIONAL_STATS_URL, timeout=30)
        response.raise_for_status()
        payload = response.json()
        return payload if isinstance(payload, list) else []

    @staticmethod
    def _load_artifact_definitions(path: Path) -> dict[str, ArtifactDefinition]:
        payload = load_json(path)
        definitions: dict[str, ArtifactDefinition] = {}
        for entry in payload:
            additional_stats = tuple(
                AdditionalStatDefinition(
                    stat_id=stat['stat_id'],
                    name_en=stat['name_en'],
                    name_ru=stat['name_ru'],
                    value=StatRangeData(min=stat['value']['min'], max=stat['value']['max']),
                )
                for stat in entry.get('additional_stats', [])
            )
            stat_ranges = {
                name: StatRangeData(min=data['min'], max=data['max'])
                for name, data in entry.get('stat_ranges', {}).items()
            }
            definitions[entry['id']] = ArtifactDefinition(
                id=entry['id'],
                name=entry['name'],
                name_ru=entry['name_ru'],
                stat_ranges=stat_ranges,
                additional_stats=additional_stats,
            )
        return definitions

    @staticmethod
    def _load_armor_definitions(path: Path) -> dict[str, ArmorDefinition]:
        payload = load_json(path)
        return {
            entry['id']: ArmorDefinition(
                id=entry['id'],
                name=entry['name'],
                name_ru=entry['name_ru'],
                stats=entry['stats'],
            )
            for entry in payload
        }

    @staticmethod
    def _load_container_definitions(path: Path) -> dict[str, ContainerDefinition]:
        payload = load_json(path)
        return {
            entry['id']: ContainerDefinition(
                id=entry['id'],
                name=entry['name'],
                name_ru=entry['name_ru'],
                protection=entry['protection'],
                efficiency=entry['efficiency'],
                capacity=entry['capacity'],
                stats=entry['stats'],
            )
            for entry in payload
        }

    @staticmethod
    def _serialize_artifacts(artifacts: dict[str, ArtifactDefinition]) -> list[dict[str, Any]]:
        return [
            {
                'id': artifact.id,
                'name': artifact.name,
                'name_ru': artifact.name_ru,
                'stat_ranges': {
                    name: {'min': stat.min, 'max': stat.max}
                    for name, stat in artifact.stat_ranges.items()
                },
                'additional_stats': [
                    {
                        'stat_id': stat.stat_id,
                        'name_en': stat.name_en,
                        'name_ru': stat.name_ru,
                        'value': {'min': stat.value.min, 'max': stat.value.max},
                    }
                    for stat in artifact.additional_stats
                ],
            }
            for artifact in artifacts.values()
        ]

    @staticmethod
    def _serialize_armors(armors: dict[str, ArmorDefinition]) -> list[dict[str, Any]]:
        return [
            {
                'id': armor.id,
                'name': armor.name,
                'name_ru': armor.name_ru,
                'stats': armor.stats,
            }
            for armor in armors.values()
        ]

    @staticmethod
    def _serialize_containers(containers: dict[str, ContainerDefinition]) -> list[dict[str, Any]]:
        return [
            {
                'id': container.id,
                'name': container.name,
                'name_ru': container.name_ru,
                'protection': container.protection,
                'efficiency': container.efficiency,
                'capacity': container.capacity,
                'stats': container.stats,
            }
            for container in containers.values()
        ]
