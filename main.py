from __future__ import annotations

from pathlib import Path
from datetime import datetime, timezone
import json
from typing import Any, Dict


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
LOG_FILE = LOG_DIR / "engine.log.txt"


# =========================
# Utilities
# =========================

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


# =========================
# Phase 0 — Lobby (minimal)
# =========================

def phase0_lobby() -> None:
    print("PHASE 0 — INITIAL SETUP")
    session = {
        "phase": 0,
        "mode": "SOLO",
        "difficulty": "EASY",
        "confirmed_utc": utc_now(),
        "turn_number": 0
    }
    save_json(SESSION_PATH, session)
    log("PHASE 0 COMPLETE (SESSION CREATED)")
    print("Session created. Re-run to continue.")


# =========================
# Phase 1 — Player Setup (stub)
# =========================

def phase1_player_setup() -> None:
    print("PHASE 1 — PLAYER SETUP (STUB)")
    session = load_json(SESSION_PATH)
    session["phase"] = 1
    save_json(SESSION_PATH, session)
    log("PHASE 1 COMPLETE")
    print("Phase 1 complete. Re-run to continue.")


# =========================
# Main Router
# =========================

def main() -> None:
    print("RISK: Global Power — Engine Start")

    # No session → Phase 0
    if not SESSION_PATH.exists():
        phase0_lobby()
        return

    session = load_json(SESSION_PATH)
    phase = session.get("phase", 0)

    # Phase 0 → Phase 1
    if phase == 0:
        phase1_player_setup()
        return

    # Phase 1 → Stop (Phase 2 not implemented yet)
    if phase == 1:
        print("Session at Phase 1.")
        print("Next station: Phase 2 (Country Selection).")
        print("Advance phase manually to test Phase 3.")
        return

    # Phase 2+ → Phase 3
    if phase >= 2:
        from phases.phase3 import run_phase_3
        run_phase_3()
        return


if __name__ == "__main__":
    main()
