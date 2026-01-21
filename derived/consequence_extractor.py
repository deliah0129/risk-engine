from __future__ import annotations

from typing import Dict, List, Any, Tuple
from dataclasses import replace
import math

from .consequence_state import (
    EvidenceItem,
    ConsequenceSignals,
    ConsequenceIndices,
    ConsequenceState,
)

# -------------------------------------------------
# Event contract (v0.1)
#
# Each event dict MAY contain:
#   turn: int
#   actor: str
#   ok: bool
#   cost: float
#   delta: float
#   magnitude: float
#
# Missing values are treated as 0 / False.
# -------------------------------------------------


def _variance(values: List[float]) -> float:
    if not values:
        return 0.0
    mean = sum(values) / len(values)
    return sum((v - mean) ** 2 for v in values) / len(values)


def extract_consequences(
    events: List[Dict[str, Any]],
    *,
    current_turn: int,
    window: int = 5,
) -> Dict[str, ConsequenceState]:
    """
    Deterministically derive consequence states from historical events.
    """

    lo = current_turn - window + 1
    hi = current_turn
    turns_used = list(range(lo, hi + 1))

    # Group events by actor within window
    by_actor: Dict[str, List[Dict[str, Any]]] = {}

    for e in events:
        turn = int(e.get("turn", -10**9))
        if turn < lo or turn > hi:
            continue

        actor = str(e.get("actor", "")).strip()
        if not actor:
            continue

        by_actor.setdefault(actor, []).append(e)

    results: Dict[str, ConsequenceState] = {}

    # -------------------------
    # First pass: per-actor metrics
    # -------------------------

    for actor, actor_events in by_actor.items():
        attempts = len(actor_events)
        successes = sum(1 for e in actor_events if bool(e.get("ok", False)))
        failures = attempts - successes

        costs = [float(e.get("cost", 0.0) or 0.0) for e in actor_events]
        deltas = [float(e.get("delta", 0.0) or 0.0) for e in actor_events]
        mags = [
            float(e.get("magnitude", e.get("delta", 0.0)) or 0.0)
            for e in actor_events
        ]

        avg_cost = (sum(costs) / attempts) if attempts else 0.0
        net_delta = sum(deltas)
        outcome_variance = _variance(mags)

        signals = ConsequenceSignals(
            attempts=attempts,
            successes=successes,
            failures=failures,
            net_delta=net_delta,
            avg_cost=avg_cost,
            outcome_variance=outcome_variance,
        )

        success_rate = (successes / attempts) if attempts else 0.0

        capacity_index = (
            0.7 * success_rate
            + 0.3 * math.tanh(net_delta / 10.0)
        )

        stability_index = 1.0 / (1.0 + outcome_variance)

        risk_index = (
            (failures / attempts) if attempts else 0.0
        )
        risk_index = 0.6 * risk_index + 0.4 * math.tanh(avg_cost / 10.0)

        # Momentum: simple slope proxy across window
        per_turn_delta = {t: 0.0 for t in turns_used}
        for e in actor_events:
            per_turn_delta[int(e.get("turn"))] += float(e.get("delta", 0.0) or 0.0)

        series = [per_turn_delta[t] for t in turns_used]
        momentum_index = (
            (series[-1] - series[0]) / max(1, window - 1)
        )

        indices = ConsequenceIndices(
            capacity_index=capacity_index,
            stability_index=stability_index,
            momentum_index=momentum_index,
            risk_index=risk_index,
            dominance_index=0.0,
        )

        tags: List[str] = []
        evidence: List[EvidenceItem] = []

        if capacity_index >= 0.65 and stability_index >= 0.55:
            tags.append("STRONG")
            evidence.append(EvidenceItem(
                signal="capacity_index",
                value=capacity_index,
                threshold=0.65,
                window=window,
                turns=turns_used,
            ))

        if attempts >= max(3, window // 2) and risk_index >= 0.45:
            tags.append("AGGRESSIVE")
            evidence.append(EvidenceItem(
                signal="risk_index",
                value=risk_index,
                threshold=0.45,
                window=window,
                turns=turns_used,
            ))

        if momentum_index <= -0.5:
            tags.append("DECLINING")
            evidence.append(EvidenceItem(
                signal="momentum_index",
                value=momentum_index,
                threshold=-0.5,
                window=window,
                turns=turns_used,
            ))

        if stability_index <= 0.35:
            tags.append("UNSTABLE")
            evidence.append(EvidenceItem(
                signal="stability_index",
                value=stability_index,
                threshold=0.35,
                window=window,
                turns=turns_used,
            ))

        results[actor] = ConsequenceState(
            actor_id=actor,
            window=window,
            computed_turn=current_turn,
            signals=signals,
            indices=indices,
            tags=tags,
            evidence=evidence,
        )

    # -------------------------
    # Second pass: dominance (relative)
    # -------------------------

    if results:
        ranked: List[Tuple[str, float]] = sorted(
            ((aid, cs.indices.capacity_index) for aid, cs in results.items()),
            key=lambda x: x[1],
            reverse=True,
        )

        top_id, top_val = ranked[0]
        second_val = ranked[1][1] if len(ranked) > 1 else -1e9
        margin = top_val - second_val

        DOMINANCE_MARGIN = 0.20

        if margin >= DOMINANCE_MARGIN:
            top = results[top_id]
            new_indices = replace(top.indices, dominance_index=margin)
            new_tags = list(top.tags)
            new_evidence = list(top.evidence)

            if "DOMINANT" not in new_tags:
                new_tags.append("DOMINANT")

            new_evidence.append(EvidenceItem(
                signal="dominance_margin",
                value=margin,
                threshold=DOMINANCE_MARGIN,
