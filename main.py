from __future__ import annotations

from pathlib import Path
from datetime import datetime, timezone
import json
from typing import Any, Dict, Tuple


# -----------------------------
# Engine paths
# -----------------------------
ENGINE_ROOT = Path(__file__).parent
STATE_DIR = ENGINE_ROOT / "state"
LOG_DIR = ENGINE_ROOT / "logs"

STATE_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "engine_log.txt"
SESSION_PATH = STATE_DIR / "session.json"
PLAYERS_PATH = STATE_DIR / "players.json"


# -----------------------------
# Utilities
# -----------------------------
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


def atomic_write_json(path: Path, data: Dict[str, Any]) -> None:
    """
    Write JSON safely:
    - write to temp
    - replace target
    Prevents half-written files if the app closes mid-save.
    """
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=2), encoding="utf-8")
    tmp.replace(path)


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_mode(raw: str) -> str:
    return raw.strip().upper()


def normalize_difficulty(raw: str) -> str:
    return raw.strip().upper()


def validate_session_schema(session: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Required keys:
      phase: int (0 or 1 is fine for now)
      mode: one of ALLOWED_MODES
      difficulty: one of ALLOWED_DIFFICULTIES
      confirmed_utc: str
    """
    required = ("phase", "mode", "difficulty", "confirmed_utc")
    for k in required:
        if k not in session:
            return False, f"Missing key: {k}"

    if not isinstance(session["phase"], int):
        return False, "phase must be an int"

    mode = str(session["mode"]).upper()
    diff = str(session["difficulty"]).upper()

    if mode not in ALLOWED_MODES:
        return False, f"Invalid mode in session: {session['mode']}"
    if diff not in ALLOWED_DIFFICULTIES:
        return False, f"Invalid difficulty in session: {session['difficulty']}"

    # confirm timestamp exists (we don't strict-parse yet)
    if not isinstance(session["confirmed_utc"], str) or not session["confirmed_utc"].strip():
        return False, "confirmed_utc must be a non-empty string"

    return True, "OK"


# -----------------------------
# Phase 0 (Lobby: Mode + Difficulty + Confirm)
# -----------------------------
def phase0_lobby() -> None:
    log("ENGINE START (PHASE 0)")
    print("RISK: Global Power — Pre-Start Lobby (Phase 0)")

    # Step 1: Mode
    print("Select Game Mode: SOLO / MULTI_LOCAL / MULTI_REMOTE")
    mode = normalize_mode(input("> "))

    if mode not in ALLOWED_MODES:
        print("Invalid mode. Exiting.")
        log("PHASE 0 REJECT (INVALID MODE)")
        return

    log(f"PHASE 0 MODE SELECTED: {mode}")

    # Step 2: Difficulty
    print("Select Difficulty: EASY / NORMAL / HARD")
    difficulty = normalize_difficulty(input("> "))

    if difficulty not in ALLOWED_DIFFICULTIES:
        print("Invalid difficulty. Exiting.")
        log("PHASE 0 REJECT (INVALID DIFFICULTY)")
        return

    log(f"PHASE 0 DIFFICULTY SELECTED: {difficulty}")

    # Summary + Confirm
    print("\nSummary (Phase 0):")
    print(f"Mode: {mode}")
    print(f"Difficulty: {difficulty}")
    print("\nType CONFIRM to write session + enter Phase 1. Anything else exits.")
    gate = input("> ").strip().upper()

    if gate != "CONFIRM":
        print("No confirm. Exiting.")
        log("PHASE 0 EXIT (NO CONFIRM)")
        return

    session = {
        "phase": 0,
        "mode": mode,
        "difficulty": difficulty,
        "confirmed_utc": utc_now(),
    }
    atomic_write_json(SESSION_PATH, session)

    print(f"CONFIRMED. Session saved to {SESSION_PATH.as_posix()}")
    log("PHASE 0 CONFIRMED (SESSION WRITTEN)")
    print("Next: Phase 1 will load this file.")


# -----------------------------
# Phase 1 (Guarded): Load session → write players.json → bump session phase
# -----------------------------
def phase1_player_setup() -> None:
    print("RISK: Global Power — Phase 1 (Player Setup — GUARDED)")
    log("PHASE 1 ENTER")

    # Guard 1: session must exist
    if not SESSION_PATH.exists():
        print("No session found. Run Phase 0 first (it creates state/session.json).")
        log("PHASE 1 BLOCK (NO SESSION)")
        return

    # Guard 2: session must parse
    try:
        session = load_json(SESSION_PATH)
    except Exception as e:
        print("Session file is unreadable JSON. Fix or delete it, then rerun Phase 0.")
        log(f"PHASE 1 BLOCK (SESSION JSON ERROR): {e}")
        return

    # Guard 3: session schema must validate
    ok, why = validate_session_schema(session)
    if not ok:
        print(f"Session schema invalid: {why}")
        print("Fix state/session.json or rerun Phase 0.")
        log(f"PHASE 1 BLOCK (BAD SESSION): {why}")
        return

    # Normalize values
    session["mode"] = str(session["mode"]).upper()
    session["difficulty"] = str(session["difficulty"]).upper()

    print("\nLoaded session:")
    print(f"  Mode: {session['mode']}")
    print(f"  Difficulty: {session['difficulty']}")
    print(f"  Confirmed UTC: {session['confirmed_utc']}")
    log("PHASE 1 SESSION LOADED")

    mode = session["mode"]

    # Player model (simple + future-proof)
    players: Dict[str, Any] = {
        "phase": 1,
        "mode": mode,
        "seats_total": None,
        "humans": [],
        "ais": [],
        "created_utc": utc_now(),
    }

    # Guarded defaults per mode (stub-safe)
    if mode == "SOLO":
        # Hard guardrails:
        # - Exactly 1 human
        # - AI count is placeholder, easy to revise later
        players["seats_total"] = 6
        players["humans"] = [{"seat": 1, "type": "HUMAN", "name": "Player1"}]
        players["ais"] = [
            {"seat": 2, "type": "AI", "name": "AI_1"},
            {"seat": 3, "type": "AI", "name": "AI_2"},
            {"seat": 4, "type": "AI", "name": "AI_3"},
            {"seat": 5, "type": "AI", "name": "AI_4"},
            {"seat": 6, "type": "AI", "name": "AI_5"},
        ]
        log("PHASE 1 DEFAULTS (SOLO) APPLIED")

    elif mode == "MULTI_LOCAL":
        # Placeholder guardrails (we’ll implement real prompts later)
        players["seats_total"] = 2
        players["humans"] = [
            {"seat": 1, "type": "HUMAN", "name": "Player1"},
            {"seat": 2, "type": "HUMAN", "name": "Player2"},
        ]
        players["ais"] = []
        log("PHASE 1 DEFAULTS (MULTI_LOCAL) APPLIED")

    elif mode == "MULTI_REMOTE":
        # Placeholder guardrails (networking later)
        players["seats_total"] = 2
        players["humans"] = [
            {"seat": 1, "type": "HUMAN", "name": "Host"},
            {"seat": 2, "type": "HUMAN", "name": "Remote1"},
        ]
        players["ais"] = []
        log("PHASE 1 DEFAULTS (MULTI_REMOTE) APPLIED")

    else:
        # Should never happen due to earlier guards
        print("Internal error: unhandled mode.")
        log("PHASE 1 FAIL (UNHANDLED MODE)")
        return

    # Write players.json safely
    atomic_write_json(PLAYERS_PATH, players)
    print(f"\nPlayers saved to {PLAYERS_PATH.as_posix()}")
    print(f"  Humans: {len(players['humans'])}")
    print(f"  AIs: {len(players['ais'])}")

    # Bump session phase only after Phase 1 output exists
    session["phase"] = 1
    atomic_write_json(SESSION_PATH, session)
    log("PHASE 1 COMPLETE (PLAYERS WRITTEN, SESSION PHASE=1)")

    print("\nPhase 1 complete (guarded). Next: Country Selection (Phase 2).")


# -----------------------------
# Router
# -----------------------------
def main() -> None:
    """
    Simple router:
    - If no session exists => Phase 0
    - If session exists and phase == 0 => run Phase 1
    - If session phase >= 1 => announce Phase 2 target (stub)
    """
    if not SESSION_PATH.exists():
        phase0_lobby()
        return

    try:
        session = load_json(SESSION_PATH)
    except Exception:
        print("Session exists but is unreadable JSON. Delete state/session.json and rerun.")
        return

    phase = session.get("phase", 0)
    if phase == 0:
        phase1_player_setup()
        return

    if phase >= 1:
        print("Session already at Phase 1+.")
        print("Next station: Phase 2 (Country Selection).")
        print("Run will be updated when Phase 2 is implemented.")
        return


if __name__ == "__main__":
    main()
