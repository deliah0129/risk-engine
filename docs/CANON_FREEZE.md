# Canon Freeze Notice

## Scope
The semantics and lifecycle of `EvidenceItem` are frozen as canonical.

## Canon Source
- `docs/SEMANTICS_EVIDENCE_ITEM.md`
- Ratified by PR #5: “Define EvidenceItem semantics and lifecycle (Phase-gating)”

## Freeze Rule
- No reinterpretation, extension, or behavioral inference of `EvidenceItem`
  is permitted during Phase 2 development.
- Phase 2 MUST consume the existing semantics exactly as defined.

## Prohibited Until Further Notice
- Behavioral inference from prose
- Derived logic expansion
- Stress testing, adversarial cases, or fuzzing
- Copilot-driven semantic suggestions

## Exception Process
Only allowed via an explicit PR labeled `semantics-change`
after Phase 2 is complete.

Status: **ACTIVE**
