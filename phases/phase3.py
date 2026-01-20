from pathlib import Path
import json
from datetime import datetime, timezone

ENGINE_ROOT = Path(__file__).resolve().parents[1]      # .../risk_engine
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
    print("RISK: Global Power — Phase 3 (Initial Resources — STUB)")
    log("PHASE 3 START")

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

    # Guard: only proceed if Phase 2 completed (session.phase >= 2)
    if int(session.get("phase", 0)) < 2:
        print("Session not ready for Phase 3. (Need phase >= 2)")
        log("PHASE 3 BLOCKED (PHASE < 2)")
        return

    mode = session.get("mode", "SOLO")
    seats_total = int(players.get("seats_total", 0))
    assignments = countries.get("assignments", [])

    if seats_total <= 0 or not assignments:
        print("Invalid players/countries state.")
        log("PHASE 3 FAIL (BAD STATE)")
        return

    # STUB resource model:
    # Everyone starts equal for now. You can branch by difficulty later.
    base = {
        "money": 100,
        "military_points": 50,
        "influence_points": 25,
        "energy": 10,
        "food": 10,
        "materials": 10,
    }

    resources = {
        "phase": 3,
        "mode": mode,
        "economy_model": "STUB_EQUAL_START",
        "seats_total": seats_total,
        "by_seat": [],
        "created_utc": utc_now(),
    }

    for seat in range(1, seats_total + 1):
        country = None
        for a in assignments:
            if int(a.get("seat", -1)) == seat:
                country = a.get("country")
                break

        entry = {
            "seat": seat,
            "country": country,
            "resources": dict(base),
        }
        resources["by_seat"].append(entry)

    save_json(RESOURCES_FILE, resources)

    # advance session
    session["phase"] = 3
    save_json(SESSION_FILE, session)

    print("\nInitial Resources (stub):")
    for r in resources["by_seat"]:
        print(f"Seat {r['seat']}: {r['country']} -> {r['resources']}")

    print("\nPhase 3 complete (stub). Next: Turn Order (Phase 4).")
    log("PHASE 3 COMPLETE (STUB)")
    log("ENGINE SHUTDOWN")

if __name__ == "__main__":
    run_phase_3()
