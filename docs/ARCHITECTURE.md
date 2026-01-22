# Architecture Overview — Governed Expansion (v0.1)

This document defines how the engine may evolve after Freeze v0.1.
It describes attachment surfaces and execution boundaries, not mechanics.

## Authority
This document is subordinate to:
- FREEZE_v0_1.md
- The Execution Grammar defined in code

If a conflict exists, this document is invalid.

## Core Execution Invariants
The following rules are enforced by structure and may not be bypassed:

1. Phase execution occurs in fixed order.
2. Actions are validated before Resolution.
3. State mutation occurs only during Resolution.
4. Derived or observer-facing state does not affect legality.

## Approved Attachment Surfaces

### Phases
- New phases may be appended only after Phase 1.
- Phases may prepare data or proposals.
- Phases may not commit state directly.

### Modules
- Modules are optional, self-contained systems.
- Modules may propose effects during Resolution.
- Modules may not redefine actors, objects, verbs, phases, or authority.

### Scenarios
- Scenarios configure module enablement and evaluation context.
- Scenarios may bind AI doctrine.
- Scenarios may not introduce new rules, verbs, or objects.

## Explicit Non-Surfaces
The following are not extension points:
- Action validation logic
- Execution grammar
- State persistence format
- Governance constraints

## Overview

The Risk Engine is a deterministic, phase-based simulation engine implemented as a playable slice.
Its architecture prioritizes execution clarity, inspectability, and explicit state transitions
over feature completeness.

The engine operates as a linear execution loop that advances through clearly defined phases,
persisting runtime state between executions to support deterministic replay and auditability.

---
```text

## High-Level Execution Flow
+------------------------+
| main.py                |
| (entry point)          |
+------------------------+
            |
            v
+------------------------+
| Load / Initialize State|
| (from persisted storage)|
+------------------------+
            |
            v
+------------------------+
| Phase Dispatcher       |
| (deterministic ordering)|
+------------------------+
            |
            v
+------------------------+
| Execution Phases       |
| (phases/*.py modules)  |
|  - phase1              |
|  - phase2              |
|  - phaseN              |
+------------------------+
            |
            v
+------------------------+
| Persist Updated State  |
| + Optional Execution   |
| Logs                   |
+------------------------+
            |
            v
+------------------------+
| Program Exit           |
| (deterministic outcome)|
+------------------------+
```

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
