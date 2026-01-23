from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Dict, List


# -------------------------------------------------
# PREFLIGHT POLICY (HARD CONSTRAINTS)
# -------------------------------------------------
# ORIENTATION ONLY. This module must NOT:
# - define variables/metrics (Phase 3)
# - define transitions/collapse logic (Phase 4)
# - define actors/authority (Phase 5)
# - define turns/actions (Phase 6)
# - run scenarios (Phase 7)
#
# It MAY:
# - inspect repo wiring
# - read design docs
# - write deterministic artifacts (state + logs)
# -------------------------------------------------


REPO_ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = REPO_ROOT / "docs"
LOGS_DIR = REPO_ROOT / "logs"
STATE_DIR = LOGS_DIR / "state"

SNAPSHOT_PATH = STATE_DIR / "preflight.json"
LOG_PATH = LOGS_DIR / "preflight.log"


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def _extract_status(md_text: str) -> str:
    for raw in md_text.splitlines():
        line = raw.strip()
        if line.upper().startswith("STATUS:"):
            return line.split(":", 1)[1].strip().upper() or "UNKNOWN"
    return "UNKNOWN"


def _discover_docs() -> List[Dict[str, str]]:
    docs: List[Dict[str, str]] = []
    if not DOCS_DIR.exists():
        return docs

    for path in sorted(DOCS_DIR.glob("*.md")):
        txt = _read_text(path)
        docs.append(
            {
                "path": path.relative_to(REPO_ROOT).as_posix(),
                "status": _extract_status(txt),
                "content": txt,
            }
        )
    return docs


def _fingerprint(docs: List[Dict[str, str]]) -> str:
    h = hashlib.sha256()
    for d in docs:
        h.update(d["path"].encode("utf-8"))
        h.update(b"\n")
        h.update(d["content"].encode("utf-8"))
        h.update(b"\n---\n")
    return h.hexdigest()


def _write_deterministic_json(path: Path, payload: Dict) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_deterministic_log(path: Path, lines: List[str]) -> None:
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> int:
    print("RISK: Global Power | PREFLIGHT")
    print("MODE: ORIENTATION ONLY (non-semantic)")
    print("")

    print("STEP 1/4: Discover design artifacts")
    docs = _discover_docs()
    print(f"  - Found {len(docs)} doc(s) in /docs")

    print("STEP 2/4: Inspect STATUS lines")
    for d in docs:
        print(f"  - {d['path']} :: STATUS={d['status']}")

    print("STEP 3/4: Write deterministic artifacts (state + logs)")
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    STATE_DIR.mkdir(parents=True, exist_ok=True)

    fp = _fingerprint(docs)

    snapshot = {
        "artifact_kind": "preflight_snapshot",
        "schema_version": "0.1",
        "mode": "orientation_only",
        "docs": [{"path": d["path"], "status": d["status"]} for d in docs],
        "determinism": {
            "fingerprint_sha256": fp,
            "note": "Derived only from doc paths + full contents. No timestamps.",
        },
        "policy": {
            "semantic_execution": False,
            "variables": False,
            "transitions": False,
            "actors": False,
            "turns": False,
            "scenarios": False,
        },
    }

    _write_deterministic_json(SNAPSHOT_PATH, snapshot)

    log_lines = [
        "RISK: Global Power | PREFLIGHT LOG",
        "MODE=ORIENTATION_ONLY",
        f"FINGERPRINT_SHA256={fp}",
        f"SNAPSHOT_PATH={SNAPSHOT_PATH.relative_to(REPO_ROOT).as_posix()}",
        "NOTE: Log is overwritten each run for determinism.",
    ]
    _write_deterministic_log(LOG_PATH, log_lines)

    print(f"  - WROTE: {SNAPSHOT_PATH.relative_to(REPO_ROOT).as_posix()}")
    print(f"  - WROTE: {LOG_PATH.relative_to(REPO_ROOT).as_posix()}")
    print("")
    print("DONE: Preflight complete (no simulation executed).")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
