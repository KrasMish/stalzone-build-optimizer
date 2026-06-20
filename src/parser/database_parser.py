from typing import Any, Iterable

from src.calculator.constants import (
    ARMOR_EXCLUDE_PARAMS_RU,
    ARTIFACT_EXCLUDE_PARAMS_RU,
    CONTAINER_META_PARAMS_RU,
)
from src.calculator.stat_keys import stat_key
from src.models.armor import ArmorDefinition
from src.models.artifact import AdditionalStatDefinition, ArtifactDefinition, StatRangeData
from src.models.container import ContainerDefinition
from src.models.game_database import GameDatabase


class DatabaseParser:
    def parse_items(self, items: Iterable[dict[str, Any]], additional_stats: list[dict[str, Any]] | None = None) -> GameDatabase:
        additional_lookup = self._build_additional_lookup(additional_stats or [])
        artifacts: dict[str, ArtifactDefinition] = {}
        armors: dict[str, ArmorDefinition] = {}
        containers: dict[str, ContainerDefinition] = {}

        for item in items:
            category = item.get('category', '')
            if not isinstance(category, str):
                continue

            if 'artefact/' in category:
                artifact = self._parse_artifact(item, additional_lookup)
                artifacts[artifact.id] = artifact
            elif category.startswith('armor/') and 'device' not in category:
                armor = self._parse_armor(item)
                armors[armor.id] = armor
            elif category.startswith('containers/'):
                container = self._parse_container(item)
                containers[container.id] = container

        return GameDatabase(artifacts=artifacts, armors=armors, containers=containers)

    def _parse_armor(self, payload: dict[str, Any]) -> ArmorDefinition:
        stats: dict[str, float] = {}
        for element in self._iter_elements(payload):
            lines = element.get('name', {}).get('lines', {})
            ru_name = lines.get('ru')
            if ru_name in ARMOR_EXCLUDE_PARAMS_RU:
                continue
            if element.get('type') != 'numeric':
                continue
            value = element.get('value')
            if value is None:
                continue
            en_name = lines.get('en', ru_name)
            stats[en_name] = float(value)

        lines = payload.get('name', {}).get('lines', {})
        return ArmorDefinition(
            id=str(payload['id']),
            name=lines.get('en', payload['id']),
            name_ru=lines.get('ru', payload['id']),
            stats=stats,
        )

    def _parse_artifact(
        self,
        payload: dict[str, Any],
        additional_lookup: dict[str, list[AdditionalStatDefinition]],
    ) -> ArtifactDefinition:
        stat_ranges: dict[str, StatRangeData] = {}
        for element in self._iter_elements(payload):
            lines = element.get('name', {}).get('lines', {})
            ru_name = lines.get('ru')
            if ru_name in ARTIFACT_EXCLUDE_PARAMS_RU:
                continue

            min_value = element.get('min', element.get('value'))
            max_value = element.get('max', element.get('value'))
            if min_value is None and max_value is None:
                continue

            en_name = lines.get('en', ru_name)
            stat_ranges[en_name] = StatRangeData(
                min=float(min_value if min_value is not None else max_value),
                max=float(max_value if max_value is not None else min_value),
            )

        lines = payload.get('name', {}).get('lines', {})
        name_ru = lines.get('ru', payload['id'])
        additional_stats = tuple(additional_lookup.get(name_ru, ()))

        return ArtifactDefinition(
            id=str(payload['id']),
            name=lines.get('en', payload['id']),
            name_ru=name_ru,
            stat_ranges=stat_ranges,
            additional_stats=additional_stats,
        )

    def _parse_container(self, payload: dict[str, Any]) -> ContainerDefinition:
        protection = 0.0
        efficiency = 100.0
        capacity = 0
        stats: dict[str, float] = {}

        for element in self._iter_elements(payload):
            lines = element.get('name', {}).get('lines', {})
            ru_name = lines.get('ru')
            if ru_name == 'Вместимость':
                capacity = int(element.get('value', 0))
                continue
            if ru_name == 'Внутренняя защита':
                protection = float(element.get('value', 0))
                continue
            if ru_name == 'Эффективность':
                efficiency = float(element.get('value', 100))
                continue
            if ru_name in CONTAINER_META_PARAMS_RU:
                continue

            value = element.get('value')
            if value is None:
                continue
            en_name = lines.get('en', ru_name)
            stats[stat_key(en_name)] = float(value)

        lines = payload.get('name', {}).get('lines', {})
        return ContainerDefinition(
            id=str(payload['id']),
            name=lines.get('en', payload['id']),
            name_ru=lines.get('ru', payload['id']),
            protection=protection,
            efficiency=efficiency,
            capacity=capacity,
            stats=stats,
        )

    @staticmethod
    def _iter_elements(payload: dict[str, Any]) -> Iterable[dict[str, Any]]:
        for block in payload.get('infoBlocks', []):
            elements = block.get('elements')
            if not isinstance(elements, list):
                continue
            for element in elements:
                if isinstance(element, dict):
                    yield element

    @staticmethod
    def _build_additional_lookup(payload: list[dict[str, Any]]) -> dict[str, list[AdditionalStatDefinition]]:
        lookup: dict[str, list[AdditionalStatDefinition]] = {}

        for entry in payload:
            lines = entry.get('lines', {})
            name_ru = lines.get('ru')
            if not name_ru:
                continue

            parsed_stats: list[AdditionalStatDefinition] = []
            for stat in entry.get('additional_stats', []):
                stat_lines = stat.get('lines', {})
                value = stat.get('value', {})
                parsed_stats.append(
                    AdditionalStatDefinition(
                        stat_id=str(stat.get('id', stat_lines.get('en', ''))),
                        name_en=stat_lines.get('en', ''),
                        name_ru=stat_lines.get('ru', ''),
                        value=StatRangeData(
                            min=float(value.get('min', 0)),
                            max=float(value.get('max', 0)),
                        ),
                    )
                )

            lookup[name_ru] = parsed_stats

        return lookup
