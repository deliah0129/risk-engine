## Current State: Engine Slice (Governed Simulation Core)

This repository represents a **governed engine slice**, not a traditional “playable game demo.”

At its current stage, the project implements the **core execution infrastructure** for a larger simulation system. The focus is on correctness, rule enforcement, and safe state progression, rather than user interaction or presentation.

The engine is designed to:
- Enforce strict phase order and execution rules
- Persist and validate session state across runs
- Refuse invalid execution paths instead of attempting recovery
- Produce audit-friendly logs for inspection and testing
- Support deterministic behavior and repeatable runs

This slice is intentionally **infrastructure-first**.

---

## What “Engine Slice” Means

An *engine slice* is a minimal but complete portion of the system that can be executed end-to-end and evaluated on its own.

In practical terms, this means:
- The engine can start, halt, resume, and advance safely
- State transitions occur only at defined resolution points
- Invalid actions or phase skips are explicitly blocked
- The system can be extended without refactoring the core

This mirrors how real systems are built in practice, where control logic and governance are validated before any UI, automation, or content layers are added.

---

## What Is Intentionally Not Included (Yet)

This slice does **not** include:
- A graphical interface
- Player interaction loops
- Visualization or presentation layers
- Autonomous agents making decisions on their own

These are downstream consumers of the engine and are excluded by design, not omission.

---

## How to Run

```bash
py main.py
```

---

## Stress Testing Suite

The repository includes a comprehensive stress testing suite to validate engine performance, reliability, and deterministic behavior.

### Quick Test (Windows)

```bash
QUICK_STRESS_TEST.bat
```

### Interactive Menu (Windows)

```bash
STRESS_TEST.bat
```

### Command Line (All Platforms)

```bash
# Run all tests
python stress_test.py --test all

# Run specific test suites
python stress_test.py --test sequential --iterations 100
python stress_test.py --test concurrent --sessions 10
python stress_test.py --test persistence --cycles 50
python stress_test.py --test determinism
```

### Test Suites

1. **Sequential Throughput** - Measures execution performance and throughput
2. **Concurrent Sessions** - Tests thread safety and state isolation
3. **State Persistence** - Validates I/O performance and data integrity
4. **Determinism Verification** - Confirms reproducible behavior

Results are saved to `stress_test_results/` with detailed JSON output
