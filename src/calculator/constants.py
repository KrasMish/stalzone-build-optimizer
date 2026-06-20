from typing import Final

NEGATIVE_STAT_NAMES: Final[frozenset[str]] = frozenset(
    {
        'Radiation',
        'Psy-emissions',
        'Biological infection',
        'Bleeding',
        'Temperature',
        'Frost',
        'Burning',
    }
)

INFECTION_STAT_NAMES: Final[frozenset[str]] = frozenset(
    {
        'Radiation',
        'Psy-emissions',
        'Biological infection',
        'Temperature',
        'Frost',
    }
)

ARMOR_EXCLUDE_PARAMS_RU: Final[frozenset[str]] = frozenset(
    {
        'Вес',
        'Прочность',
        'Макс. прочность',
        'Ранг',
        'Класс',
        'Эффективность',
    }
)

ARTIFACT_EXCLUDE_PARAMS_RU: Final[frozenset[str]] = frozenset(
    {
        'Заряд',
        'Макс. заряд',
        'Срабатывает при',
        'Снижает урон на',
        'Перезарядка',
        'Заряда за активации',
        'Качество',
        'Вес',
    }
)

CONTAINER_META_PARAMS_RU: Final[frozenset[str]] = frozenset(
    {
        'Вес',
        'Эффективность',
        'Ранг',
        'Класс',
        'Вместимость',
        'Внутренняя защита',
    }
)

EXBO_DATABASE_RAW_URL: Final[str] = (
    'https://raw.githubusercontent.com/EXBO-Studio/stalcraft-database/main/ru'
)
