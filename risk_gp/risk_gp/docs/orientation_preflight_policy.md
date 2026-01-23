# Orientation Preflight Policy (v0.1)
STATUS: COMPLETE

## Purpose
Preflight provides a deterministic, non-semantic execution path that proves repo wiring,
governance discipline, and artifact hygiene before gameplay semantics exist.

## Classification
Orientation / Instrumentation  
This is NOT a simulation run.

## Allowed Behavior
Preflight MAY:
- inspect repository structure
- read design documents in `/docs`
- report STATUS lines
- write deterministic artifacts to `/logs/state/` and `/logs/`

## Prohibited Behavior (Non-negotiable)
Preflight MUST NOT:
- define variables or metrics (Phase 3)
- define transitions, collapse, or recovery rules (Phase 4)
- define actors or authority (Phase 5)
- define turns or actions (Phase 6)
- run scenarios, including any “10 turn” scenario (Phase 7)

## Determinism Standard
Outputs must be deterministic:
- derived only from file paths and file contents
- no timestamps
- overwrite artifacts each run to prevent drift
