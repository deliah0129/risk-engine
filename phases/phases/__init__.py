from pathlib import Path
import json
from typing import Dict, Any

STATE_DIR = Path("state")
SESSION_PATH = STATE_DIR / "session.json"
PLAYERS_PATH = STATE_DIR / "players.json"


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data: Dict[str, Any]) -> None:
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def run_phase1() -> None:
    print("=== Phase 1: Player Setup ===")

    if not SESSION_PATH.exists():
        raise FileNotFoundError(
            "Missing session.json. Run Phase 0 first (python main.py)."
        )

    session = load_json(SESSION_PATH)

    # Minimal validation
    if session.get("phase") != 0:
        raise ValueError(f"Expected session phase 0, got {session.get('phase')}")

    # Create default SOLO player state
    players = {
        "players": [
            {
                "id": "P1",
                "type": "HUMAN",
                "name": "Player 1"
            }
        ]
    }

    save_json(PLAYERS_PATH, players)

    # Advance phase
    session["phase"] = 1
    save_json(SESSION_PATH, session)

    print("[OK] players.json written")
    print("[OK] session advanced to Phase 1")
    print("Next: Phase 2")
