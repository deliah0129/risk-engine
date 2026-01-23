# ==============================
# CI / Proof Run Guard
# ==============================
import os
import sys

def _truthy(name: str) -> bool:
    return os.getenv(name, "").strip().lower() in {"1", "true", "yes", "on"}

RUN_MODE = os.getenv("RISK_RUN_MODE", "").strip().lower()
IS_CI = _truthy("CI")

PROOF_MODE = RUN_MODE == "proof" or (IS_CI and RUN_MODE != "normal")

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
# Router
# =========================

def main() -> None:
    if not SESSION_FILE.exists():
        print("No session found. Run Phase 0 first.")
        log("ROUTER: NO SESSION")
        return

    session = load_json(SESSION_FILE)
    phase = int(session.get("phase", -1))

    # ---- Phase routing ----

    # Phase 1 → Country Selection (Phase 2 stub)
    if phase == 1:
        from phases.phase2 import run_phase_2
        run_phase_2()
        return

    # Phase 2 → Initial Resources (Phase 3)
    if phase == 2:
        from phases.phase3 import run_phase_3
        run_phase_3()
        return

    # Phase 3 → Turn Order (Phase 6)
    if phase == 3:
        from phases.phase6 import run_phase_6
        run_phase_6()
        return

    print(f"Unknown session phase: {phase}")
    log(f"ROUTER: UNKNOWN PHASE {phase}")


# =========================
# Entry
# =========================

if __name__ == "__main__":
    main()


