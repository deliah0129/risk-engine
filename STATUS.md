# STATUS — risk-engine

**Project:** risk-engine  
**Current Version:** v0.2  
**Status:** Stable / Archived-Ready  
**Last Updated:** 2026-01-23  

---

## Project State Summary

`risk-engine` is a deterministic strategy simulation **engine core**, developed as a governed system slice.

As of **v0.2**, the engine:
- executes bounded turns,
- enforces ordered phase execution,
- mutates state only at controlled commit points,
- and fails deterministically when collapse conditions are met.

All guarantees are validated automatically via CI.

This repository is considered **complete for its stated scope**.

---

## Version Milestones

### v0.1 — Governed Engine Slice
- Phase-based execution established
- Persistent state and session routing implemented
- Invalid execution paths explicitly refused
- Proof-only CI validation added
- Scope frozen via `FREEZE_v0_1.md`

### v0.2 — Turn Semantics & Failure Validation (Current)
- Explicit turn semantics defined and enforced
- Deterministic scenario execution added:
  - Stable
  - Stressed
  - Collapse
- Collapse treated as a **valid terminal outcome**
- Failure is observable, intentional, and governed
- CI validates success and failure paths with zero failed jobs
- Scope frozen via `FREEZE_v0_2.md`

---

## What This Repository Is

- A **validated system core**
- A reference implementation of:
  - deterministic execution,
  - temporal governance,
  - and controlled failure
- A teaching / review artifact suitable for inspection without author context

---

## What This Repository Is Not

The following are intentionally **out of scope** and deferred:

- Player actions or choices
- AI or autonomous agents
- UI or visualization layers
- Narrative or balance tuning
- Real-world predictive claims
- Expansion beyond the core engine loop

Any future work must occur on a new version and issue a new freeze document.

---

## CI & Validation Posture

- GitHub Actions executes:
  - proof runs,
  - stable scenarios,
  - stressed scenarios,
  - deterministic collapse scenarios
- Collapse exits non-zero **by design** and is asserted as correct behavior
- Overall CI health is green with **0% job failure rate**

CI is authoritative for engine correctness at this scope.

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

## Stop Rule

The project is **complete at v0.2**.

No additional features, mechanics, or structural changes may be added without:
- incrementing the version, and
- issuing a new freeze document.

This repository may be safely:
- archived,
- taught from,
- reviewed,
- or extended via a new development branch.

---

**End of STATUS**
