# StalZone Build Optimizer

AI-assisted optimizer for STALCRAFT:X artifact builds.

## Features

- EXBO database sync for artifacts, armor, and containers
- Artifact stat scaling ported from the community build calculator engine
- Price grouping by quality rarity for RU/EU market files
- Configurable validation limits and optimization weights
- Playstyle presets and custom priority overrides
- Top-N build generation with budget filtering

## Quick start

```bash
python -m pip install -e .
python -m src.main --sync-db --region RU --budget 50000000 --top-n 5
```

Populate `data/prices/ru.json` before optimizing:

```json
{
  "region": "RU",
  "artifacts": {
    "artifact_id": {
      "rare": 3250000,
      "epic": 4100000
    }
  }
}
```

Or store raw sales and let the price parser aggregate them:

```json
{
  "artifacts": {
    "artifact_id": {
      "sales": [
        {"quality": 137, "upgrade": 15, "price": 3250000, "sold_at": "2026-06-19T12:00:00+00:00"}
      ]
    }
  }
}
```

## CLI options

- `--sync-db` refresh EXBO cache into `data/processed/`
- `--region RU|EU`
- `--budget` maximum build price
- `--armor` / `--container` EXBO item ids
- `--quality` default artifact quality percentage
- `--playstyle tank|speed|hybrid|carry`
- `--priority carry_weight:10,vitality:8`
- `--max-candidates 10000`

## Architecture

- `src/parser/` EXBO and price parsing
- `src/calculator/` official-style build formulas
- `src/optimizer/` validation, scoring, candidate generation
- `src/market/` price storage and rarity grouping
- `src/ai/advisor.py` build explanations only

## Tests

```bash
python -m unittest discover -s tests
```
