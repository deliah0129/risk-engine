RISK ENGINE — PROJECT RULES (CANONICAL)

1. SCOPE DISCIPLINE
   - This project prioritizes execution integrity over feature breadth.
   - No feature is added without a clear purpose, attachment point, and constraint.
   - MVP means “structurally complete,” not “content complete.”

2. GOVERNANCE FIRST
   - All execution follows explicit phase boundaries.
   - Invalid actions are prevented, not corrected after the fact.
   - The system must resist misuse by both players and designers.

3. DETERMINISM
   - Identical inputs must always produce identical outcomes.
   - No hidden randomness, implicit state, or silent side effects.
   - All resolution paths must be traceable and explainable.

4. STATE TRANSPARENCY
   - Runtime state is explicit, persisted, and inspectable.
   - No “magic” transitions or background automation.
   - Logs exist to explain behavior, not decorate it.

5. SEPARATION OF CONCERNS
   - Engine logic, content, and interface are strictly separated.
   - UI, UX, and presentation layers are out of scope unless explicitly added later.
   - Content depth does not define system completeness.

6. RESTRAINT BY DESIGN
   - Features may be intentionally absent if they weaken clarity or stability.
   - Expansion is deferred unless the core loop remains intact.
   - Future growth must preserve the established execution model.

7. EDUCATIONAL & PROFESSIONAL LEGIBILITY
   - The project must be readable by juniors, seniors, and reviewers.
   - Design intent should be inferable from structure alone.
   - Documentation explains “why,” not just “what.”

8. VERSIONING & FINALITY
   - Each release is complete at its declared layer.
   - Version bumps signal intent, not polish.
   - No silent changes; scope shifts must be explicit.
