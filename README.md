RISK ENGINE — RULES FOR CONTRIBUTORS

Welcome. This project is intentionally structured and constrained.
That is not an accident, and it is not a test.

If you’re contributing, here’s how to succeed without breaking things.

1. THIS IS AN ENGINE, NOT A FINISHED GAME
   - You are working on the core execution system.
   - Missing features, UI, and content are intentional.
   - Do not add things “just to make it more fun.”

2. READ BEFORE YOU WRITE CODE
   - Take time to understand the execution phases and core loop.
   - Trace how state moves from input → resolution → update.
   - If you don’t understand where something fits, pause and ask.

3. DO NOT BYPASS RULES
   - If the system prevents an action, that is by design.
   - Do not hack around constraints or force state changes.
   - If something feels blocked, the correct response is analysis, not shortcuts.

4. ONE CHANGE AT A TIME
   - Make small, focused changes.
   - Be able to explain exactly what your change does and why it exists.
   - If you can’t explain it clearly, it’s not ready to add.

5. KEEP IT DETERMINISTIC
   - Same inputs must always produce the same outcome.
   - No hidden randomness, no silent side effects.
   - If behavior can’t be explained step-by-step, it doesn’t belong.

6. DON’T MIX LAYERS
   - Engine logic stays separate from content and presentation.
   - UI, visuals, and polish are out of scope unless explicitly approved.
   - Clean structure matters more than clever tricks.

7. BREAKING THINGS IS OK — SILENTLY BREAKING THINGS IS NOT
   - It’s fine to experiment.
   - It’s not fine to change behavior without documenting it.
   - If something fails, it should fail clearly and visibly.

8. WHEN IN DOUBT, ASK
   - This system rewards careful thinking, not speed.
   - Questions are expected.
   - Guessing is how systems get damaged.

If you follow these rules, you will:
- Learn real systems design skills
- Avoid subtle bugs
- Contribute safely and meaningfully

If you ignore them, the system will fight you.
That’s normal. Slow down and re-align.
