# Risk Engine — Playable Slice v0.1

This repository contains a deterministic strategy simulation engine implemented as a playable slice.

The system is designed around **explicit phase boundaries**, **persisted runtime state**, and **governance-style constraints**. The focus of this version is execution integrity and structural clarity rather than feature completeness.

This release is intended to be readable, auditable, and extensible by engineers evaluating deterministic or rules-driven systems.

---

## Requirements

- Python 3.x
- Windows (for `RUN_RISK_ENGINE.bat`), or any platform with Python CLI support

No external Python dependencies are required for v0.1.

---

## How to Run (Windows)

1. Download or clone this repository.
2. Double-click `RUN_RISK_ENGINE.bat`.

This will invoke the engine using the local Python installation.

---

## How to Run (Manual)

From the repository root:

```bash
python main.py
---
```
## Expected Output

On first run, the engine will:

- Prompt for game mode and difficulty (Phase 0)
- Persist a session file to `state/session.json`
- On confirmation, advance to Phase 1 and generate `state/players.json`

Subsequent runs resume from persisted state and advance the phase router accordingly.

---

## Resetting the Engine

To reset the engine to a clean state, delete the `state/` directory.

All runtime state is regenerated deterministically from user input.

---

## State & Logs

- Persistent state is stored in `state/` as JSON files
- Runtime logs are written to `logs/engine_log.txt`

State files are authoritative. Logs are diagnostic only.
