import json
from pathlib import Path

from derived.consequence_extractor import extract_consequences
from tests.fixtures import sample_events


def _golden_path_for(window: int) -> Path:
    base = Path(__file__).parent / "golden"

    # Keep your existing v0.1 golden name for window=5
    if window == 5:
        return base / "consequences_turn_10.json"

    return base / f"consequences_turn_10_window_{window}.json"


def test_consequence_extraction_matches_goldens_across_windows():
    events = sample_events()

    for window in (3, 5, 10):
        results = extract_consequences(
            events,
            current_turn=10,
            window=window,
        )

        golden = json.loads(_golden_path_for(window).read_text())

        observed = {
            actor: {"tags": state.tags}
            for actor, state in results.items()
        }

        assert observed == golden, (
            f"Consequence extraction drift detected (window={window}).\n"
            f"Observed: {observed}\n"
            f"Expected: {golden}"
        )
