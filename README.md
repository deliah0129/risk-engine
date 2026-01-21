## Scope

This project implements a small, deterministic execution core for a turn-based strategy simulation.

The engine is limited to a few early phases that establish session state, player configuration, and initial world assignment. These phases are designed to run exactly once, persist their results to disk, and advance the system into a clearly defined next state. There is no looping, rollback, or automatic progression.

Systems such as combat, economy, diplomacy, and AI decision-making are intentionally not included. Their absence keeps the focus on execution order, state validation, and persistence mechanics rather than on gameplay outcomes.

The intent is to make the system’s behavior easy to reason about: given the same inputs and phase order, the engine produces the same results and records them explicitly. This slice exists to explore structure, constraints, and failure modes before layering additional mechanics on top.
