# RISK Engine — Deterministic Strategy Simulation (Playable Slice v0.1)

## Overview

This repository contains a **deterministic, phase-based strategy simulation engine** implemented as a playable slice.  
The project is intentionally scoped to emphasize **systems design, execution integrity, and state governance** rather than feature completeness.

The engine is structured around **explicit phase boundaries**, **persisted runtime state**, and **guarded execution paths**.  
Each phase is treated as a transactional unit: once completed, its results are written to disk and become the sole input for subsequent phases.

This design prioritizes correctness, auditability, and reproducibility over interactivity or UI complexity.

---

## Educational Purpose

This project is designed to demonstrate and teach **systems thinking**, not just programming syntax.

Specifically, it illustrates:

- Deterministic execution models  
- Explicit state transitions and persistence  
- Phase-based transaction boundaries  
- Guardrails that prevent invalid or out-of-order execution  
- Separation of source code from runtime artifacts  

Unlike many academic projects that focus on algorithms in isolation, this engine models **how real systems behave over time** and under constraints.

---

## Architectural Principles

### Phase-Based Execution

The engine progresses through numbered phases.  
Each phase:

- Has a single responsibility  
- Is executed exactly once per run  
- Writes its results to disk  
- Advances the session state explicitly  

Phases do **not** loop or auto-chain. This is intentional.

This mirrors real-world systems where:
- execution is non-reversible
- state must be validated before use
- partial completion is a failure mode

---

### Persisted Runtime State

All meaningful runtime data is written to the `state/` directory as structured JSON.

Examples include:
- `session.json` — global session metadata and phase tracking
- `players.json` — player configuration from Phase 1
- `countries.json` — ownership assignments from Phase 2

State files are **outputs**, not configuration inputs, and are therefore excluded from version control.

This enforces a clear distinction between:
- *source of truth* (code)
- *derived artifacts* (runtime state)

---

### Guarded Execution

The engine enforces strict ordering:

- Phases cannot be skipped
- Invalid inputs cause immediate termination
- Execution halts rather than auto-correcting user behavior

This reflects defensive programming practices used in safety-critical and transactional systems.

---

## Current Implementation Status

### Implemented Phases

- **Phase 0 — Session Creation**
  - Game mode selection
  - Difficulty selection
  - Session initialization

- **Phase 1 — Player Setup**
  - Human and AI player registration
  - Deterministic player configuration
  - Persisted to `state/players.json`

- **Phase 2 — Country Assignment**
  - Deterministic assignment of countries to players
  - Ownership persistence
  - Session advances to Phase 3

### Not Yet Implemented

- Phase 3 and beyond (combat, economy, diplomacy, etc.)  
These are intentionally deferred until the foundational execution model is complete and stable.

---

## What This Project Is (and Is Not)

**This project is:**
- A systems architecture exercise
- A deterministic simulation engine
- A teaching tool for execution integrity

**This project is not:**
- A complete game
- A UI-focused application
- An AI behavior showcase

The absence of features is deliberate and documented.

---

## How to Run (Windows)

1. Clone or download the repository
2. Double-click `RUN_RISK_ENGINE.bat`
3. Follow the on-screen prompts

The batch file ensures the engine is executed from the correct working directory.

---

## Design Philosophy

The engine is intentionally resistant to:
- accidental misuse
- out-of-order execution
- silent failure

If the engine exits, it is signaling an invalid state or input — not a crash.

This philosophy mirrors real-world systems where
