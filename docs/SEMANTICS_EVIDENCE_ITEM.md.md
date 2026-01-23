# EvidenceItem Semantics

## Purpose
EvidenceItem represents immutable explanatory data that justifies a computed consequence.
It exists to support determinism, traceability, and post-hoc inspection.

EvidenceItem is not a resource handle, process, or stateful object.
It owns no external resources and requires no cleanup.

## Creation
- EvidenceItem instances are created only during consequence extraction.
- Creation occurs within the derived layer.
- EvidenceItem creation must be deterministic given identical inputs.

## Mutability
- EvidenceItem is immutable after creation.
- No field may be modified once instantiated.

## Ownership
- EvidenceItem instances are owned by the consequence snapshot that references them.
- They are not shared across consequences except by value copy.

## Lifetime
- EvidenceItem lifetime is bound to the lifetime of the consequence snapshot.
- When a consequence snapshot is discarded, its EvidenceItems are discarded.
- No global registry or external lifecycle management is required.

## Storage & Serialization
- EvidenceItem must be serializable as plain data (e.g. JSON).
- EvidenceItem must not depend on runtime-only objects.
- Field ordering and presence must be stable once frozen.

## Constraints
- EvidenceItem must not implement close(), context management, or resource hooks.
- If an object requires cleanup, it is not an EvidenceItem.

## Freeze Rule
EvidenceItem semantics are frozen once consequence grammar and turn resolution order are finalized.
Any change after freeze requires an explicit version bump.
