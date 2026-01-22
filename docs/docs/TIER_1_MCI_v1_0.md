# Tier-1 Protocol — Manifest Compliance Interface (MCI) v1.0

**Status:** ACTIVE  
**Tier:** 1 (Protocol)  
**Scope:** Compliance and extension governance only

## Purpose
This protocol defines the only legal ways to extend the system after Freeze v0.1.
It prevents ontology drift and protects execution invariants.

This document governs all Tier-2 artifacts (modules, scenarios, mechanics).

## Authority
This document is subordinate to:
- The System Manifest
- FREEZE_v0_1.md

If a conflict exists, this document is invalid.

## Core Invariants (Non-Negotiable)
The following must remain true at all times:

1. Actor classes are fixed.
2. Object classes are fixed.
3. Verbs are a closed canon.
4. Phase 0 (grammar OFF) and Phase 1 (grammar ON) semantics may not be altered.
5. State mutation occurs only during Resolution.
6. Quantities are non-negative integers only.
7. Derived or observer-facing state does not affect legality.
8. AI doctrine selects among legal actions only; it cannot justify outcomes.

Violation of any invariant invalidates the artifact.

## Allowed Extension Surfaces

### S-1: Module Effects Proposal
Modules may:
- Read immutable and mutable state
- Propose effects as data

Modules may not:
- Commit state directly
- Redefine actors, objects, verbs, phases, or authority
- Bypass validation or resolution

### S-2: Scenario Configuration
Scenarios may:
- Enable or disable modules
- Bind AI doctrine
- Modify evaluation or termination context

Scenarios may not:
- Introduce new verbs or objects
- Modify execution grammar
- Override validation rules

## Forbidden Actions
The following are explicitly forbidden:

- Mutating state outside Resolution
- Retroactive state modification
- Bypassing legality checks
- Introducing narrative, strategy, or intent interpretation
- Granting automatic success or failure

## Compliance Declaration (Required)
Every Tier-2 artifact must declare:

- Extension surface used (S-1 or S-2)
- State read set
- State write set (effects only for modules)
- Invariant checklist (PASS/FAIL)

Artifacts without a declaration are invalid by default.

## Enforcement
Non-compliant artifacts:
- Must not execute
- Must not alter state
- Must be rejected at load or validation time
