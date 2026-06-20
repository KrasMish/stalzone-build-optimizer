from pathlib import Path
from typing import Any

from src.utils.json_utils import load_json


class WikiParser:
    def __init__(self, source_path: Path) -> None:
        self.source_path = source_path

    def parse(self) -> dict[str, Any]:
        if not self.source_path.exists():
            return {}
        payload = load_json(self.source_path)
        return payload if isinstance(payload, dict) else {'items': payload}
