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
    required = ("phase", "mode", "difficulty", "confirmed_utc", "turn_number")
    for k in required:
        if k not in session:
            return False, f"Missing key: {k}"

    if not isinstance(session["phase"], int):
        return False, "phase must be int"

    if session["mode"] not in ALLOWED_MODES:
        return False, "invalid mode"

    if session["difficulty"] not in ALLOWED_DIFFICULTIES:
        return False, "invalid difficulty"

    if not isinstance(session["turn_number"], int):
        return False, "turn_number must be int"

    return True, "OK"

# =========================
# Phase 0 — Lobby
# =========================

def phase0_lobby() -> None:
    print("RISK: Global Power — Phase 0 (Lobby)")
    log("PHASE 0 START")

    mode = input("Select Mode (SOLO / MULTI_LOCAL / MULTI_REMOTE): ").strip().upper()
    if mode not in ALLOWED_MODES:
        print("Invalid mode.")
        return

    difficulty = input("Select Difficulty (EASY / NORMAL / HARD): ").strip().upper()
    if difficulty not in ALLOWED_DIFFICULTIES:
        print("Invalid difficulty.")
        return

    confirm = input("Type CONFIRM to start game: ").strip().upper()
    if confirm != "CONFIRM":
        print("Cancelled.")
        return

    session = {
        "phase": 0,
        "mode": mode,
        "difficulty": difficulty,
        "confirmed_utc": utc_now(),
        "turn_number": 0,
    }

    save_json(SESSION_PATH, session)
    log("PHASE 0 CONFIRMED")
    print("Session created.")

# =========================
# Phase 1 — Player Setup
# =========================

def phase1_player_setup() -> None:
    print("RISK: Global Power — Phase 1 (Player Setup)")
    log("PHASE 1 START")

    session = load_json(SESSION_PATH)

    players: Dict[str, Any] = {
        "phase": 1,
        "mode": session["mode"],
        "seats_total": 6 if session["mode"] == "SOLO" else 2,
        "humans": [],
        "ais": [],
        "created_utc": utc_now(),
    }

    if session["mode"] == "SOLO":
        players["humans"] = [{"seat": 1, "type": "HUMAN", "name": "Player"}]
        players["ais"] = [
            {"seat": i, "type": "AI", "name": f"AI_{i}"}
            for i in range(2, 7)
        ]

    save_json(PLAYERS_PATH, players)

    session["phase"] = 1
    save_json(SESSION_PATH, session)

    log("PHASE 1 COMPLETE")
    print("Players initialized.")

# =========================
# Phase 2 — Country Selection (STUB)
# =========================

def phase2_country_selection() -> None:
    print("RISK: Global Power — Phase 2 (Country Selection — STUB)")
    log("PHASE 2 START")

    players = load_json(PLAYERS_PATH)

    assignments = []
    for seat in range(1, players["seats_total"] + 1):
        assignments.append({
            "seat": seat,
            "country": f"Country_{seat}"
        })

    countries = {
        "phase": 2,
        "assignments": assignments,
        "created_utc": utc_now(),
    }

    save_json(COUNTRIES_PATH, countries)

    session = load_json(SESSION_PATH)
    session["phase"] = 2
    save_json(SESSION_PATH, session)

    log("PHASE 2 COMPLETE")
    print("Countries assigned.")

# =========================
# Phase 3 — Turn Skeleton
# =========================

def phase3_turn() -> None:
    print("PHASE 3 — TURN SKELETON")
    log("PHASE 3 START")

    session = load_json(SESSION_PATH)
    ok, why = validate_session_schema(session)
    if not ok:
        print(f"Invalid session: {why}")
        return

    turn = session["turn_number"]
    print(f"TURN START: {turn}")
    log(f"TURN START {turn}")

    # NO-OP input
    log("INPUT: NO_OP")

    # NO-OP resolution
    log("RESOLUTION: NO_OP")

    session["turn_number"] += 1
    save_json(SESSION_PATH, session)

    print(f"TURN COMPLETE: {session['turn_number']}")
    log("PHASE 3 END")

# =========================
# Router
# =========================

def main() -> None:
    if not SESSION_PATH.exists():
        phase0_lobby()
        return

    session = load_json(SESSION_PATH)
    phase = session.get("phase", 0)

    if phase == 0:
        phase1_player_setup()
    elif phase == 1:
        phase2_country_selection()
    elif phase >= 2:
        phase3_turn()

# =========================

if __name__ == "__main__":
    main()
