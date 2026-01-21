## Scope

This project implements a small, deterministic execution model for a turn-based strategy simulation.

At this stage, the engine is limited to a few foundational phases that establish session state, player definitions, and initial territory ownership. Each phase is executed once, in a fixed order, and produces persisted state that becomes the input for the next phase. There is no rollback, branching, or automatic progression beyond what is explicitly defined.

Systems such as combat resolution, economic modeling, diplomacy, and longer-term decision logic are intentionally not implemented yet. Excluding these systems keeps attention on execution order, state transitions, and persistence rather than on gameplay depth.

The purpose of this slice is to make system behavior explicit and inspectable. Given the same inputs and phase sequence, the engine produces the same outcomes, and those outcomes are recorded directly in the runtime state files. This makes it easier to reason about how the system moves from one state to the next before adding additional mechanics.
