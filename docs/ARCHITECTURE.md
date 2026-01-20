# Risk Engine — Architecture Overview (v0.1)

## Overview

The Risk Engine is a deterministic, phase-based simulation engine implemented as a playable slice.
Its architecture prioritizes execution clarity, inspectability, and explicit state transitions
over feature completeness.

The engine operates as a linear execution loop that advances through clearly defined phases,
persisting runtime state between executions to support deterministic replay and auditability.

---

## High-Level Execution Flow

┌───────────────────────────┐
│           main.py         │
│        (entry point)      │
└─────────────┬─────────────┘
              │
              v
┌───────────────────────────┐
│   Load / Initialize State │
│  (from persisted storage)│
└─────────────┬─────────────┘
              │
              v
┌───────────────────────────┐
│     Phase Dispatcher      │
│  (deterministic ordering) │
└─────────────┬─────────────┘
              │
              v
┌───────────────────────────┐
│     Execution Phases      │
│   (phases/*.py modules)   │
│   - phase1                │
│   - phase2                │
│   - phaseN                │
└─────────────┬─────────────┘
              │
              v
┌───────────────────────────┐
│   Persist Updated State   │
│   + Optional Execution    │
│           Logs            │
└─────────────┬─────────────┘
              │
              v
┌───────────────────────────┐
│        Program Exit       │
│  (deterministic outcome)  │
└───────────────────────────┘

---

## Core Design Principles

### Phase-Based Execution
- Each phase represents a discrete step in the simulation lifecycle.
- Phases are executed sequentially and intentionally kept simple.
- New behavior is introduced by adding phases, not modifying control flow.

### Deterministic State
- Runtime state is persisted to disk between executions.
- State persistence enables replay, inspection, and debugging.
- No hidden or implicit in-memory state is relied upon across runs.

### Governance-Oriented Structure
- Execution rules are explicit rather than emergent.
- Predictability and traceability are favored over dynamic behavior.
- The system is suitable for experimentation with rule-driven engines.

---

## Non-Goals (v0.1)

- No user interface
- No content-complete simulation
- No performance or scalability optimization
- No automated test suite beyond environment validation

These constraints are intentional and define the scope of the playable slice.

---

## Extension Points

Future iterations may introduce:
- Additional execution phases
- Scenario or rule modules
- State validation layers
- Alternative persistence backends

All extensions are expected to preserve the deterministic execution model.
