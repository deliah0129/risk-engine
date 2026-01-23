from pathlib import Path
import json
from datetime import datetime, timezone

ENGINE_ROOT = Path(__file__).resolve().parents[1]  # .../risk_engine
STATE_DIR = ENGINE_ROOT / "state"
LOG_DIR = ENGINE_ROOT / "logs"
STATE_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

SESSION_FILE = STATE_DIR / "session.json"
PLAYERS_FILE = STATE_DIR / "players.json"
COUNTRIES_FILE = STATE_DIR / "countries.json"
RESOURCES_FILE = STATE_DIR / "resources.json"
LOG_FILE = LOG_DIR / "engine_log.txt"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def log(msg: str) -> None:
    prev = LOG_FILE.read_text(encoding="utf-8") if LOG_FILE.exists() else ""
    LOG_FILE.write_text(prev + f"[{utc_now()}] {msg}\n", encoding="utf-8")


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, obj) -> None:
    path.write_text(json.dumps(obj, indent=2), encoding="utf-8")


def run_phase_3() -> None:
    print("RISK: Global Power — Phase 3 (Initial Resources — STRUCTURE ONLY)")
    log("PHASE 3 START")

    # Required upstream artifacts
    if not SESSION_FILE.exists():
        print("Missing state/session.json. Run Phase 0 first.")
        log("PHASE 3 FAIL (NO SESSION)")
        return

    if not PLAYERS_FILE.exists():
        print("Missing state/players.json. Run Phase 1 first.")
        log("PHASE 3 FAIL (NO PLAYERS)")
        return

    if not COUNTRIES_FILE.exists():
        print("Missing state/countries.json. Run Phase 2 first.")
        log("PHASE 3 FAIL (NO COUNTRIES)")
        return

    session = load_json(SESSION_FILE)
    players = load_json(PLAYERS_FILE)
    countries = load_json(COUNTRIES_FILE)

    # Strict gate: Phase 3 only runs when Phase 2 is complete and current
    phase = int(session.get("phase", 0))
    if phase != 2:
        print(f"Phase 3 blocked. Expected session.phase == 2, got {phase}.")
        log(f"PHASE 3 BLOCKED (PHASE != 2) phase={phase}")
        return

    if RESOURCES_FILE.exists():
        print("resources.json already exists. Refusing to overwrite (governance).")
        log("PHASE 3 BLOCKED (RESOURCES EXISTS)")
        return

    mode = session.get("mode", "SOLO")
    seats_total = int(players.get("seats_total", 0))
    assignments = countries.get("assignments", [])

    if seats_total <= 0:
        print("Invalid players state: seats_total <= 0.")
        log(f"PHASE 3 FAIL (BAD SEATS) seats_total={seats_total}")
        return

    if not isinstance(assignments, list) or len(assignments) == 0:
        print("Invalid countries state: assignments missing/empty.")
        log("PHASE 3 FAIL (NO ASSIGNMENTS)")
        return

    # Build seat -> country mapping
    seat_to_country = {}
    for a in assignments:
        try:
            seat = int(a.get("seat"))
        except Exception:
            seat = None
        country = (a.get("country") or "").strip() if isinstance(a, dict) else ""
        if seat is None or seat <= 0:
            continue
        seat_to_country[seat] = country

    # Validate seat coverage + uniqueness + country presence
    expected_seats = set(range(1, seats_total + 1))
    actual_seats = set(seat_to_country.keys())
    missing = sorted(expected_seats - actual_seats)
    extra = sorted(actual_seats - expected_seats)

    if missing or extra:
        print(f"Invalid assignments. missing={missing} extra={extra}")
        log(f"PHASE 3 FAIL (ASSIGNMENTS MISMATCH) missing={missing} extra={extra}")
        return

    missing_countries = [s for s in sorted(expected_seats) if not seat_to_country.get(s)]
    if missing_countries:
        print(f"Invalid assignments. Missing country names for seats: {missing_countries}")
        log(f"PHASE 3 FAIL (MISSING COUNTRY NAMES) seats={missing_countries}")
        return

    # Structure-only initial bundle (equal start)
    ruleset = {
        "starting_budget": 10,
        "starting_units": 0,
        "starting_influence": 0
    }

    resources = {
        "phase": 3,
        "mode": mode,
        "economy_model": "EQUAL_START_STRUCTURE_ONLY",
        "created_utc": utc_now(),
        "ruleset": ruleset,
        "resources_by_seat": []
    }

    for seat in range(1, seats_total + 1):
        entry = {
            "seat": seat,
            "country": seat_to_country[seat],
            "wallet": {
                "budget": ruleset["starting_budget"],
                "units": ruleset["starting_units"],
                "influence": ruleset["starting_influence"]
            },
            "ledger": []
        }
        resources["resources_by_seat"].append(entry)

    save_json(RESOURCES_FILE, resources)

    # Advance session
    session["phase"] = 3
    save_json(SESSION_FILE, session)

    print("\nInitial Resources (structure-only):")
    for r in resources["resources_by_seat"]:
        print(f"Seat {r['seat']}: {r['country']} -> {r['wallet']}")

    print("\nPhase 3 complete. Next: Turn Order (Phase 4).")
    log("PHASE 3 COMPLETE (STRUCTURE ONLY)")
    log("ENGINE SHUTDOWN")


if __name__ == "__main__":
    run_phase_3()
