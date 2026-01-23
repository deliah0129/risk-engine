# FREEZE_v0_2 — Governed Turn Semantics & Failure Validation

**Project:** risk-engine  
**Version:** v0.2  
**Status:** FROZEN  
**Date:** 2026-01-23  

---

## Scope Summary

Version v0.2 formalizes **turn semantics** and **deterministic failure behavior** for the risk-engine core.

This version builds on the v0.1 governed engine slice by explicitly defining:
- bounded execution in time (turns),
- controlled state mutation points,
- and intentional, observable system failure.

No gameplay, UI, agents, or balancing logic are introduced in this version.

---

## What Changed from v0.1

### 1. Turn Semantics (Phase 6)
- Execution is now explicitly bounded into **turns**.
- Each turn has:
  - a defined start,
  - ordered phase execution,
  - a single state commit point.
- State mutation outside of turn execution is disallowed by construction.

### 2. Deterministic Scenarios (Phase 7)
Three scripted scenarios are defined and executed automatically:
- **Stable:** no degradation, no collapse.
- **Stressed:** controlled degradation without collapse.
- **Collapse:** deterministic failure at a fixed turn.

### 3. Intentional Failure Handling
- Collapse is a **valid terminal outcome**, not an error.
- Collapse emits an explicit `COLLAPSE` signal.
- Collapse exits with a non-zero code intentionally.

### 4. CI Validation
- GitHub Actions validates all scenarios automatically.
- CI asserts that:
  - stable and stressed scenarios complete successfully,
  - collapse occurs when expected,
  - failure is observable and contained.
- Overall CI health remains green with zero failed jobs.

---

## What This Version Proves

- The engine understands **time** via turns.
- The engine enforces **order and boundaries**.
- The engine can **fail deterministically and correctly**.
- Failure is **tested, observable, and governed**, not accidental.

This establishes the engine as a **validated system core**, not just executable code.

---

## Explicit Non-Goals (Deferred)

The following are intentionally **out of scope** for v0.2:
- Player actions or choices
- AI or autonomous agents
- UI or visualization
- Narrative or balance tuning
- Real-world predictive claims
- Expansion beyond the core engine loop

All future work must build on v0.2 without violating its guarantees.

---

## Stop Rule

v0.2 is complete.

No additional features, mechanics, or structural changes may be added without:
- incrementing the version,
- and issuing a new freeze document.

This version may be safely archived, taught from, or extended via a new development branch.

---

**End of FREEZE_v0_2**
