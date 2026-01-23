from pathlib import Path
import json
import random
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
TURN_ORDER_FILE = STATE_DIR / "turn_order.json"
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


def run_phase_4() -> None:
    print("RISK: Global Power — Phase 4 (Turn Order — STRUCTURE ONLY)")
    log("PHASE 4 START")

    # Required upstream artifacts
    if not SESSION_FILE.exists():
        print("Missing state/session.json. Run Phase 0 first.")
        log("PHASE 4 FAIL (NO SESSION)")
        return
    if not PLAYERS_FILE.exists():
        print("Missing state/players.json. Run Phase 1 first.")
        log("PHASE 4 FAIL (NO PLAYERS)")
        return
    if not COUNTRIES_FILE.exists():
        print("Missing state/countries.json. Run Phase 2 first.")
        log("PHASE 4 FAIL (NO COUNTRIES)")
        return
    if not RESOURCES_FILE.exists():
        print("Missing state/resources.json. Run Phase 3 first.")
        log("PHASE 4 FAIL (NO RESOURCES)")
        return

    session = load_json(SESSION_FILE)
    players = load_json(PLAYERS_FILE)
    countries = load_json(COUNTRIES_FILE)

    # Governance: strict phase gate
    phase = int(session.get("phase", 0))
    if phase != 3:
        print(f"Phase 4 blocked. Expected session.phase == 3, got {phase}.")
        log(f"PHASE 4 BLOCKED (PHASE != 3) phase={phase}")
        return

    # Governance: refuse overwrite
    if TURN_ORDER_FILE.exists():
        print("state/turn_order.json already exists. Refusing to overwrite (governance).")
        log("PHASE 4 BLOCKED (TURN_ORDER EXISTS)")
        return

    seats_total = int(players.get("seats_total", 0))
    if seats_total <= 0:
        print("Invalid players state: seats_total <= 0.")
        log(f"PHASE 4 FAIL (BAD SEATS) seats_total={seats_total}")
        return

    # Optional validation: assignments cover seats 1..N exactly once
    assignments = countries.get("assignments", [])
    seat_to_country = {}
    if isinstance(assignments, list):
        for a in assignments:
            if not isinstance(a, dict):
                continue
            try:
                s = int(a.get("seat"))
            except Exception:
                continue
            c = (a.get("country") or "").strip()
            if s > 0:
                seat_to_country[s] = c

    expected = set(range(1, seats_total + 1))
    actual = set(seat_to_country.keys())
    if expected != actual or any(not seat_to_country.get(s) for s in expected):
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        missing_names = [s for s in sorted(expected) if not seat_to_country.get(s)]
        print("Invalid seat assignments for turn order.")
        print(f"  missing seats: {missing}")
        print(f"  extra seats:   {extra}")
        print(f"  missing names: {missing_names}")
        log(f"PHASE 4 FAIL (ASSIGNMENTS INVALID) missing={missing} extra={extra} missing_names={missing_names}")
        return

    # Deterministic seed: prefer session.seed; else derive & store one
    seed = session.get("seed")
    if seed is None:
        # stable enough but still explicit: derive from created_utc if present, else timestamp
        base = session.get("created_utc") or utc_now()
        seed = abs(hash(base)) % (2**31)
        session["seed"] = seed
        save_json(SESSION_FILE, session)
        log(f"PHASE 4 NOTE (SEED STORED) seed={seed}")

    rng = random.Random(int(seed))

    order = list(range(1, seats_total + 1))
    rng.shuffle(order)

    turn_order = {
        "phase": 4,
        "mode": session.get("mode", "SOLO"),
        "method": "SEEDED_SHUFFLE",
        "seed": int(seed),
        "seats_total": seats_total,
        "order": order,
        "seat_to_country": {str(k): seat_to_country[k] for k in sorted(seat_to_country.keys())},
        "created_utc": utc_now(),
    }

    save_json(TURN_ORDER_FILE, turn_order)

    # Advance session
    session["phase"] = 4
    save_json(SESSION_FILE, session)

    print("\nTurn Order (seeded):")
    for i, s in enumerate(order, start=1):
        print(f"{i}. Seat {s}: {seat_to_country[s]}")

    print("\nPhase 4 complete (structure-only). Next: Turn Frame (Phase 5).")
    log("PHASE 4 COMPLETE (STRUCTURE ONLY)")
    log("ENGINE SHUTDOWN")


if __name__ == "__main__":
    run_phase_4()
