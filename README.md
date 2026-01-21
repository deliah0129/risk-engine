## Overview

This repository contains the core of a phase-driven simulation engine designed to prioritize correctness, traceability, and controlled system evolution. The current implementation focuses on establishing a reliable execution spine rather than domain complexity.

The system advances through explicitly defined phases and maintains all runtime state in a persisted form, allowing execution to be safely paused, resumed, or repeated without loss of consistency.

## Design Notes

Several constraints guide the structure of the engine:

- Execution order is explicit rather than implicit
- State changes are isolated and persisted at defined boundaries
- Progression is monotonic and restart-safe
- Invalid or incomplete state prevents further execution

These choices favor inspectability and reliability over feature density, providing a stable foundation for future expansion.

## Current Scope

At this stage, the engine implements a minimal turn cycle and supporting phase control. Higher-level systems such as decision logic, simulation depth, and user interaction are intentionally deferred in order to validate the core execution model first.

## Status

The current version represents a validated baseline suitable for extension. Additional systems are expected to layer on top of this structure without altering its core guarantees.
