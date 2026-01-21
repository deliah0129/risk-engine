import json
from pathlib import Path

from derived.consequence_extractor import extract_consequences
from tests.fixtures import sample_events


def test_consequence_extraction_matches_golden():
    events = sample_events()

    results = extract_consequences(
        events,
        current_turn=10,
        window=5,
    )

    snapshot_path = (
        Path(__file__).parent / "golden" / "consequences_turn_10.json"
    )
    golden = json.loads(snapshot_path.read_text())

    observed = {
        actor: {"tags": state.tags}
        for actor, state in results.items()
    }

    assert observed == golden, (
        "Consequence extraction drift detected.\n"
        f"Observed: {observed}\n"
        f"Expected: {golden}"
    )
