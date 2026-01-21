Risk Engine — Playable Slice v0.1

This repository contains a verified, playable slice of a deterministic strategy
simulation engine.

This release represents a complete implementation of the engine’s foundational
layer: a phase-based execution loop, persisted runtime state, and explicit
governance constraints. The focus is execution integrity and structural clarity,
not feature completeness.

The system is intentionally designed to make invalid or ambiguous execution
difficult by default. All state transitions are ordered, auditable, and governed
by explicit rules.

What this release is:
- A deterministic, phase-governed simulation engine core
- A stateful execution loop with enforced ordering
- A rules- and constraints-first architecture
- A stable foundation suitable for extension or evaluation

What this release is not:
- A finished game
- A UI-driven application
- A content-complete simulation

Those layers are deliberately out of scope for this version.

Intended use:
- Systems and engine design exploration
- Deterministic simulation experimentation
- Governance- and rules-driven architecture work
- Educational, evaluative, or professional reference

Future releases may expand scenarios, tooling, or interfaces while preserving
the core execution model established here.

Status:
- Version: v0.1
- Scope: Foundational playable slice
- Stability: Verified
