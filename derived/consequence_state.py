from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Any


# -----------------------------
# Evidence (why a consequence exists)
# -----------------------------

@dataclass(frozen=True)
class EvidenceItem:
    signal: str
    value: float
    threshold: Optional[float] = None
    window: Optional[int] = None
    turns: Optional[List[int]] = None
    note: Optional[str] = None


# -----------------------------
# Raw signals (measured, windowed)
# -----------------------------

@dataclass(frozen=True)
class ConsequenceSignals:
    attempts: int = 0
    successes: int = 0
    failures: int = 0

    net_delta: float = 0.0
    avg_cost: float = 0.0
    outcome_variance: float = 0.0


# -----------------------------
# Derived indices (normalized)
# -----------------------------

@dataclass(frozen=True)
class ConsequenceIndices:
    capacity_index: float = 0.0
    stability_index: float = 0.0
    momentum_index: float = 0.0
    risk_index: float = 0.0

    # Relative, computed after all actors evaluated
    dominance_index: float = 0.0


# -----------------------------
# First-class derived consequence state
# -----------------------------

@dataclass(frozen=True)
class ConsequenceState:
    actor_id: str
    window: int
    computed_turn: int

    signals: ConsequenceSignals = field(default_factory=ConsequenceSignals)
    indices: ConsequenceIndices = field(default_factory=ConsequenceIndices)

    # Human-readable labels (derived only, never authored)
    tags: List[str] = field(default_factory=list)

    # Receipts for explainability / audits
    evidence: List[EvidenceItem] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
