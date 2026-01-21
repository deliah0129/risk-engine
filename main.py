from __future__ import annotations

from pathlib import Path
from datetime import datetime, timezone
import json
from typing import Any, Dict, Tuple

# =========================
# Engine Paths
# =========================

ENGINE_ROOT = Path(__file__).parent
STATE_DIR = ENGINE_ROOT / "state"
LOG_DIR = ENGINE_ROOT / "logs"

STATE_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

SESSION_PATH = STATE_DIR / "session.json"
PLAYERS_PATH = STATE_DIR / "players.json"
COUNTRIES_PATH = STATE_DIR / "countries.json"
RESOURCES_PATH = STATE_DIR / "resources.json"
LOG_FILE = LOG_DIR / "engine.log.txt"

# =========================
# Utilities
# =========================

ALLOWED_MODES = {"SOLO", "MULTI_LOCAL", "MULTI_REMOTE"}
ALLOWED_DIFFICULTIES = {"EASY", "NORMAL", "HARD"}

def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()

def log(msg: str) -> None:
    line = f"[{utc_now()}] {msg}\n"
    if LOG_FILE.exists():
        LOG_FILE.write_text(LOG_FILE.read_text(encoding="utf-8") + line, encoding="utf-8")
    else:
        LOG_FILE.write_text(line, encoding="utf-8")

def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))

def save_json(path: Path, data: Dict[str, Any]) -> None:
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")

def validate_session_schema(session: Dict[str, Any]) -> Tuple[bool, str]:
    r
