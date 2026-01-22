# Freeze v0.1 — Engine Slice (Governed Simulation Core)

**Status:** FROZEN  
**Scope:** Execution infrastructure only (no mechanics, no strategy, no automation).

## What is included (v0.1)
- Deterministic, phase-based execution order
- Persisted state files (session + phase outputs)
- Governance constraints enforced by structure and documentation
- Minimal runnable entry point (CLI/script)

## What is explicitly NOT included (v0.1)
- Combat resolution, economy simulation, diplomacy mechanics, technology mechanics
- AI strategy, coaching, hinting, probabilistic narration
- UI/UX, networking, optimization, balancing

## Non-negotiable invariants
- State changes occur only at Resolution
- Invalid actions produce no state change
- Quantities are non-negative integers only
- Modules may not redefine actors, objects, verbs, phases, or authority

## Change control
Any change that alters the invariants or scope requires:
- version bump (v0.1 → v0.2)
- entry in CHANGELOG
- updated docs for affected components
