# risk-engine

This is a hobby project exploring a deterministic strategy simulation engine.

I’m interested in what happens when you strip a strategy game down to:
- explicit phases
- clearly defined state
- reproducible outcomes

There’s no UI, no polish, and no finished “game” here yet — that’s intentional.
Right now this repo is about structure and mechanics, not presentation.

## What’s here

The engine runs through a small number of clearly separated phases.
Each phase has a specific job and operates on explicit state.

The focus is on:
- determinism (same input → same outcome)
- inspectable state
- predictable resolution order

If something feels overly explicit, that’s on purpose.

## What this is *not*

This is not:
- a playable game
- a finished engine
- a performance benchmark
- a comparison to commercial strategy games

Those might come later, or they might not. That’s fine.

## Repo layout (roughly)

- `main.py` — entry point
- `phases/` — phase-by-phase execution logic
- `state/` — serialized game/session state
- `logs/` — runtime output for inspection
- `tests/` — checks around determinism and behavior

## Current status

This project is actively tinkered with.
Some parts are solid, others are evolving.

If you want a clearer snapshot of where things stand right now, see `STATUS.md`.

## Why I’m building this

Mostly because I enjoy:
- systems that explain themselves
- engines that are easy to reason about
- simulations where outcomes aren’t mysterious

If you’re curious, feel free to poke around.
