from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


# ==========================================================
# Paths / Files
# ==========================================================
ROOT = Path(__file__).resolve().parent
STATE_DIR = ROOT / "state"
LOG_DIR = ROOT / "logs"

SESSION_FILE = STATE_DIR / "session.json"
PLAYERS_FILE = STATE_DIR / "players.json"
COUNTRIES_FILE = STATE_DIR / "countries.json"

LOG_DIR.mkdir(exist_ok=True)
STATE_DIR.mkdir(exist_ok=True)


# ==========================================================
# Utilities
# ==========================================================
def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_json(path: Path) -> Any:
    if not path.exists():
        raise FileNotFoundError(f"Missing required file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def safe_exit(msg: str = "") -> None:
    if msg:
        print(msg)
    sys.exit(0)


def get_phase(session: Dict[str, Any]) -> int:
    # Supports a few common variants without refactoring earlier files.
    for k in ("phase", "current_phase", "phase_index"):
        v = session.get(k)
        if isinstance(v, int):
            return v
        if isinstance(v, str) and v.isdigit():
            return int(v)
    raise ValueError("session.json missing phase (expected: phase/current_phase/phase_index).")


def set_phase(session: Dict[str, Any], new_phase: int) -> None:
    for k in ("phase", "current_phase", "phase_index"):
        if k in session:
            session[k] = new_phase
            return
    session["phase"] = new_phase


def load_or_none(path: Path) -> Optional[Any]:
    try:
        return read_json(path)
    except FileNotFoundError:
        return None


def normalize_choice(s: str) -> str:
    return (s or "").strip().lower()


# ==========================================================
# Phase 0: Pre-Start Lobby (Session creation)
# ==========================================================
def run_phase_0() -> None:
    print("RISK: Global Power - Pre-Start Lobby (Phase 0)")
    print("Select Game Mode: SOLO / MULTI_LOCAL / MULTI_REMOTE")
    mode = normalize_choice(input("> "))

    if mode not in ("solo", "multi_local", "multi_remote"):
        safe_exit("Invalid mode. Exiting.")

    print("Select Difficulty: EASY / NORMAL / HARD")
    difficulty = normalize_choice(input("> "))

    if difficulty not in ("easy", "normal", "hard"):
        safe_exit("Invalid difficulty. Exiting.")

    # Minimal session payload; Phase 2 uses this for deterministic seeding if available.
    session: Dict[str, Any] = {
        "session_id": f"sess_{utc_now()}",
        "created_at": utc_now(),
        "mode": mode.upper(),
        "difficulty": difficulty.upper(),
        "phase": 0,
    }

    print("")
    print("Summary (Phase 0):")
    print(f"Mode: {session['mode']}")
    print(f"Difficulty: {session['difficulty']}")
    print("")
    print("Type CONFIRM to write session + enter Phase 1. Anything else exits.")
    confirm = normalize_choice(input("> "))

    if confirm != "confirm":
        safe_exit("Exiting without saving session.")

    # Advance to phase 1 and persist
    set_phase(session, 1)
    write_json(SESSION_FILE, session)

    print(f"CONFIRMED. Session saved to {SESSION_FILE.as_posix()}")
    print("Next: Phase 1 will load this file.")
    # End process cleanly (your current UX appears to stop after each guarded phase)
    return


# ==========================================================
# Phase 1: Player Setup (Guarded)
# ==========================================================
@dataclass(frozen=True)
class Player:
    id: str
    kind: str  # "HUMAN" or "AI"


def _build_players_for_mode(session: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Minimal, runtime-first player setup with deterministic structure.
    No AI behavior yet, just identity entries.
    """
    mode = str(session.get("mode", "")).upper()

    # SOLO: 1 human + 1 AI baseline (minimal playable slice)
    if mode == "SOLO":
        return [
            {"id": "HUMAN_1", "kind": "HUMAN"},
            {"id": "AI_1", "kind": "AI"},
        ]

    # MULTI_LOCAL: ask for human count (2-6), no AI by default
    if mode == "MULTI_LOCAL":
        print("Enter number of local human players (2-6):")
        raw = normalize_choice(input("> "))
        if not raw.isdigit():
            safe_exit("Invalid player count. Exiting.")
        n = int(raw)
        if n < 2 or n > 6:
            safe_exit("Player count out of range. Exiting.")
        return [{"id": f"HUMAN_{i+1}", "kind": "HUMAN"} for i in range(n)]

    # MULTI_REMOTE: placeholder, still creates 2 humans minimum
    if mode == "MULTI_REMOTE":
        # Keep it deterministic and minimal: assume 2 humans until remote wiring exists
        return [
            {"id": "HUMAN_1", "kind": "HUMAN"},
            {"id": "HUMAN_2", "kind": "HUMAN"},
        ]

    safe_exit("Invalid mode. Exiting.")
    return []


def run_phase_1() -> None:
    print("RISK: Global Power - Phase 1 (Player Setup - GUARDED)")

    session = load_or_none(SESSION_FILE)
    if not isinstance(session, dict):
        safe_exit(f"Missing or invalid session file: {SESSION_FILE.as_posix()}")

    phase = get_phase(session)
    if phase != 1:
        safe_exit("Invalid mode. Exiting.")  # Mirrors your screenshot behavior

    players = _build_players_for_mode(session)

    print("")
    print("Summary (Phase 1):")
    print(f"Players: {len(players)}")
    for p in players:
        print(f"- {p['id']} ({p['kind']})")
    print("")
    print("Type CONFIRM to write players + enter Phase 2. Anything else exits.")
    confirm = normalize_choice(input("> "))

    if confirm != "confirm":
        safe_exit("Exiting without saving players.")

    write_json(PLAYERS_FILE, {"players": players})

    # Advance to Phase 2
    set_phase(session, 2)
    write_json(SESSION_FILE, session)

    print(f"CONFIRMED. Players saved to {PLAYERS_FILE.as_posix()}")
    print("Phase 1 complete (guarded). Next: Country Selection (Phase 2).")
    return


# ==========================================================
# Phase 2: Country Selection (Dispatch only; logic lives in phases/phase2.py)
# ==========================================================
def run_phase_2_dispatch() -> None:
    # Keep the import inside the function to avoid import-time side effects.
    from phases.phase2 import run_phase_2  # noqa: WPS433

    result = run_phase_2()
    print("Phase 2 complete.")
    print(result)
    return


# ==========================================================
# Phase 3: Stub (untouched)
# ==========================================================
def run_phase_3_dispatch() -> None:
    # If you later add run_phase_3(), this will pick it up.
    try:
        from phases.phase3 import run_phase_3  # type: ignore
    except Exception:
        print("RISK: Global Power - Phase 3 (stub)")
        print("Phase 3 exists but has no callable entry point yet.")
        return

    # If present, call it
    result = run_phase_3()  # type: ignore
    print("Phase 3 complete.")
    print(result)


# ==========================================================
# Main dispatcher (minimal, guarded, runtime-first)
# ==========================================================
def main() -> None:
    # If session doesn't exist, start at Phase 0.
    session = load_or_none(SESSION_FILE)
    if session is None:
        run_phase_0()
        return

    if not isinstance(session, dict):
        safe_exit("Invalid session.json format. Exiting.")

    phase = get_phase(session)

    if phase == 0:
        # You normally won’t see this unless someone manually edits session.json.
        run_phase_0()
        return

    if phase == 1:
        run_phase_1()
        return

    if phase == 2:
        run_phase_2_dispatch()
        return

    if phase == 3:
        run_phase_3_dispatch()
        return

    safe_exit(f"Unknown phase '{phase}'. Exiting.")


if __name__ == "__main__":
    main()
