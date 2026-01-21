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
