from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict


def load_json(file_path: str | Path) -> Dict[str, Any]:
    path = Path(file_path).expanduser().resolve()
    if not path.exists():
        raise FileNotFoundError(f"JSON file not found: {path}")
    with path.open("r", encoding="utf-8") as fp:
        return json.load(fp)