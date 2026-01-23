# STATUS — risk-engine

**Project:** risk-engine  
**Current Version:** v0.2  
**Status:** Stable (active development continues)  
**Last Updated:** 2026-01-23  

---

## Project State Summary

`risk-engine` is a deterministic strategy simulation **engine core**, developed as a governed system slice.

As of **v0.2**, the engine:
- executes explicitly bounded turns,
- enforces ordered phase execution,
- mutates state only at controlled commit points,
- and handles collapse as a deterministic, valid terminal outcome.

These guarantees are validated automatically via CI.

The project remains **actively developed**, with v0.2 serving as a stable baseline for future versions.

---

## Version Milestones

### v0.1 — Governed Engine Slice
- Phase-based execution established
- Persistent state and session routing implemented
- Invalid execution paths explicitly refused
- Proof-only CI validation added
- Scope frozen via `FREEZE_v0_1.md`

### v0.2 — Turn Semantics & Failure Validation (Current Baseline)
- Explicit turn semantics defined and enforced
- Deterministic scenario execution added:
  - Stable (no degradation)
  - Stressed (controlled degradation)
  - Collapse (deterministic failure at a fixed turn)
- Collapse treated as a **valid terminal outcome**, not an error
- Failure is observable, intentional, and governed
- CI validates both success and failure paths with zero failed jobs
- Scope frozen via `FREEZE_v0_2.md`

---

## What This Repository Is

- A **validated engine core**
- A foundation for future expansion into:
  - actors and authority,
  - decision-making systems,
  - higher-level simulation logic
- A reference implementation of:
  - deterministic execution,
  - temporal governance,
  - controlled and testable failure

---

## What This Repository Is Not (Yet)

The following remain intentionally **out of scope** as of v0.2:

- Player-facing gameplay
- AI or autonomous agents
- UI or visualization layers
- Narrative or balance tuning
- Real-world predictive claims

These elements may be introduced in **future versions** without retroactively altering v0.2 guarantees.

---

## CI & Validation Posture

- GitHub Actions executes:
  - proof runs,
  - stable scenarios,
  - stressed scenarios,
  - deterministic collapse scenarios
- Collapse exits non-zero **by design** and is asserted as correct behavior
- CI health is authoritative and currently reports **0% job failure**

---

## Logs Directory

The `logs/` directory contains **illustrative runtime output** from early engine execution
and CI validation.

These files:
- are not canonical artifacts,
- do not represent authoritative simulation state,
- and are provided solely to demonstrate execution trace behavior.

Logs should not be interpreted as results or datasets.

---

## Version Discipline & Stop Rules

Each version of `risk-engine` is explicitly scoped and frozen via a corresponding
`FREEZE_vX_Y.md` document.

Completion of **v0.2**:
- establishes a stable, validated baseline,
- does **not** imply cessation of development,
- and does **not** prohibit future work.

All future development must:
- increment the version,
- preserve v0.2 guarantees,
- and issue a new freeze document upon completion.

---

## Current Posture

- v0.2 is complete and stable.
- The project remains active.
- Further work proceeds forward by version, not by mutation.

---

**End of STATUS**
