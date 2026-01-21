RISK ENGINE — RULES FOR CONTRIBUTORS (JUNIOR-FRIENDLY)

Welcome! This project is not a typical class assignment or game repo.
Before you change anything, read these rules. They exist to help you
succeed without breaking the system.

---

1. WHAT THIS PROJECT IS
- A deterministic strategy simulation engine.
- A system designed to be predictable, inspectable, and hard to misuse.
- A foundation, not a finished game.

If you are looking to add UI, graphics, balance, or lots of content,
this is not the place (yet).

---

2. WHAT YOU SHOULD DO FIRST
- Read the Core Loop overview.
- Identify where your change would live (engine, module, or content).
- Ask: “What problem does this solve?”

If you cannot answer that question clearly, stop and ask.

---

3. WHAT YOU ARE ALLOWED TO CHANGE
You MAY:
- Clarify or improve existing logic.
- Add content that follows existing rules.
- Refactor code for clarity without changing behavior.
- Propose new ideas (see Rule 7).

You may work on ONE thing at a time.

---

4. WHAT YOU MUST NOT DO
Do NOT:
- Add randomness without approval.
- Skip execution phases.
- Introduce hidden state or background behavior.
- Add features “just to see what happens.”
- Change multiple systems at once.

If your change makes the system harder to reason about, it is wrong.

---

5. DETERMINISM RULE (IMPORTANT)
Given the same inputs, the system must behave the same way every time.

If your change breaks determinism, it will be rejected.

---

6. THINK IN STATES, NOT FEATURES
This system is built around:
- Explicit state
- Explicit transitions
- Explicit outcomes

Avoid “magic” behavior.
If you can’t explain what state changed and why, rethink the change.

---

7. HOW TO PROPOSE A NEW IDEA
Before adding anything new, write down:
- The purpose (what problem it solves)
- Where it attaches in the system
- What it costs or restricts

Ideas without constraints will not be accepted.

---

8. KEEP IT READABLE
Assume the next person reading your code is tired.
Favor clarity over cleverness.
Comments should explain “why,” not narrate the code.

---

9. WHEN IN DOUBT
Stop.
Ask.
Do not guess.

This project rewards careful thinking more than fast coding.

---

10. FINAL NOTE
Breaking things accidentally is normal.
Breaking rules intentionally is not.

If you follow these rules, you will learn a lot.
