# RISK: Global Power  
**Design-Only. Deterministic by Construction.**

This project is a controlled simulation of how governments **hold together or fall apart** over time.

It is not a prediction engine.  
It is not a political argument.  
It is not an AI guessing the future.

It is a **structural stress test**.

---

## What problem this project solves

Most simulations jump straight to behavior and outcomes.  
This one does not.

It asks a simpler, more careful question:

> What does a government structurally need to survive, and what happens when those supports weaken?

Everything in this repo exists to answer that question **without lying to itself**.

---

## What this project is (and is not)

**This project is:**
- a design-first simulation
- deterministic (same inputs → same outputs)
- built in strict phases
- focused on structure, not ideology
- slow on purpose so later results are trustworthy

**This project is not:**
- a prediction of real-world events
- a moral judgment of governments
- a real-time AI system
- a finished game (yet)

---

## The core model (plain English)

Every government depends on a small set of structural supports.  
If enough of them fail, the system collapses.

This project tracks **seven universal pillars**:

1. **Legitimacy** — Do people accept the authority as real enough to obey?
2. **Control of force** — Can violence be contained?
3. **Resources** — Is there money, labor, and material to operate?
4. **Administration** — Can decisions actually be carried out?
5. **Territory** — Is claimed territory truly controlled?
6. **Information** — Can the system communicate and coordinate?
7. **Elite support** — Are powerful insiders still cooperating?

These are treated as **load-bearing columns**, not gamey stats.

---

## Why the project is built in phases

Each phase answers exactly one type of question.

You are not allowed to skip ahead.

- **Phase 1:** Define the system
- **Phase 2:** Define what it universally requires
- **Phase 3:** Translate requirements into variables
- **Phase 4:** Define states and collapse conditions
- **Phase 5:** Define who can act
- **Phase 6:** Define turn structure
- **Phase 7:** Stress-test scenarios
- **Phase 8–9:** Reflection and stop

This discipline exists to prevent false precision and scope drift.

---

## The 60-second experience (first impressions count)

This repo intentionally includes a **structure-only preflight**.

Preflight exists to prove that:
- the project runs end-to-end
- execution is deterministic
- state and logs are written correctly
- no gameplay or behavior is happening yet

### Run preflight
```bash
python -m risk_gp.preflight
