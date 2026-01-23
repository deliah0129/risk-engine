# ==============================
# CI / Proof Run Guard (v0.2-ready)
# ==============================
import os
import sys

def _truthy(name: str) -> bool:
    return os.getenv(name, "").strip().lower() in {"1", "true", "yes", "on"}

RUN_MODE = os.getenv("RISK_RUN_MODE", "").strip().lower()
IS_CI = _truthy("CI")

# v0.2: if we're running a scenario, DO NOT short-circuit.
RISK_SCENARIO = os.getenv("RISK_SCENARIO", "").strip().lower()

PROOF_MODE = (RISK_SCENARIO == "") and (RUN_MODE == "proof" or (IS_CI and RUN_MODE != "normal"))

if PROOF_MODE:
    print("Proof run OK (observer-only). No state created.")
    sys.exit(0)

from pathlib import Path
import json
from datetime import datetime, timezone

# =========================
# Paths
# =========================
ENGINE_ROOT = Path(__file__).resolve().parent
STATE_DIR = ENGINE_ROOT / "state"
LOG_DIR = ENGINE_ROOT / "logs"

STATE_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

SESSION_FILE = STATE_DIR / "session.json"
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

def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))

def save_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")

# =========================
# v0.2 Scenario Runner (Phase 6–7)
# =========================
def run_v0_2_scenario(*, scenario: str, turns: int, seed: int) -> int:
    """
    Minimal Phase 6–7 harness:
      - runs bounded turns
      - writes deterministic JSON into /state
      - prints BEGIN TURN / END TURN
      - prints COLLAPSE for collapse scenario
    Returns exit code: 0 for success, 1 for intentional collapse.
    """
    scenario = scenario.strip().lower()
    if scenario not in {"stable", "stressed", "collapse"}:
        print(f"Unknown scenario: {scenario!r}")
        return 2

    # Deterministic state artifact for v0.2 (separate from your real session lifecycle)
    state_path = STATE_DIR / "v0_2_scenario.json"

    pillars = {
        "legitimacy": 100,
        "control_of_violence": 100,
        "resource_extraction": 100,
        "administrative_capacity": 100,
        "territorial_control": 100,
        "information_control": 100,
        "elite_coalition_management": 100,
    }

    scenario_state = {
        "version": "v0.2",
        "scenario": scenario,
        "seed": seed,
        "turns_planned": turns,
        "turn": 0,
        "pillars": pillars,
        "collapse": False,
        "collapse_turn": None,
    }

    save_json(state_path, scenario_state)

    collapse = False
    collapse_turn = None

    for t in range(1, turns + 1):
        print(f"BEGIN TURN {t}/{turns} scenario={scenario}")
        log(f"TURN_BEGIN t={t} scenario={scenario}")

        # Deterministic per-scenario evolution
        if scenario == "stable":
            pass

        elif scenario == "stressed":
            # gradual strain, no collapse within 10 turns
            scenario_state["pillars"]["resource_extraction"] -= 3  # ends at 70
            scenario_state["pillars"]["information_control"] -= 2  # ends at 80

        elif scenario == "collapse":
            # deterministic collapse at a fixed turn (turn 5)
            scenario_state["pillars"]["legitimacy"] -= 20
            if scenario_state["pillars"]["legitimacy"] <= 0 and not collapse:
                collapse = True
                collapse_turn = t

        scenario_state["turn"] = t
        scenario_state["collapse"] = collapse
        scenario_state["collapse_turn"] = collapse_turn

        save_json(state_path, scenario_state)

        print(f"END TURN {t}/{turns} collapse={collapse}")
        log(f"TURN_END t={t} collapse={collapse}")

        if collapse:
            print("COLLAPSE")
            log(f"COLLAPSE t={t}")
            return 1

    return 0

# =========================
# Router
# =========================
def main() -> None:
    # v0.2 scenarios run independently of Phase 0 session gating
    scenario = os.getenv("RISK_SCENARIO", "").strip().lower()
    if scenario:
        turns = int(os.getenv("RISK_TURNS", "10"))
        seed = int(os.getenv("RISK_SEED", "1337"))
        rc = run_v0_2_scenario(scenario=scenario, turns=turns, seed=seed)
        sys.exit(rc)

    # ---- existing router unchanged below ----
    if not SESSION_FILE.exists():
        print("No session found. Run Phase 0 first.")
        log("ROUTER: NO SESSION")
        return

    session = load_json(SESSION_FILE)
    phase = int(session.get("phase", 0))

    # ---- Phase 3: Turn Skeleton ----
    if phase >= 2:
        from phases.phase3 import run_phase_3
        run_phase_3()
        return

    # ---- Phase 2 placeholder ----
    if phase == 1:
        print("Session already at Phase 1.")
        print("Next station: Phase 2 (Country Selection).")
        print("Run will be updated when Phase 2 is implemented.")
        log("ROUTER: PHASE 1 STUB")
        return

    print("Unknown session phase.")
    log("ROUTER: UNKNOWN PHASE")

# =========================
# Entry
# =========================
if __name__ == "__main__":
    main()
