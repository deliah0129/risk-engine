import json
from pathlib import Path

from derived.consequence_extractor import extract_consequences
from tests.fixtures import sample_events


def main() -> None:
    base = Path(__file__).parent / "golden"
    base.mkdir(parents=True, exist_ok=True)

    events = sample_events()

    # Keep v0.1 file name as the canonical window=5 golden
    windows = (3, 5, 10)

    for window in windows:
        results = extract_consequences(events, current_turn=10, window=window)

        observed = {
            actor: {"tags": state.tags}
            for actor, state in results.items()
        }

        if window == 5:
            path = base / "consequences_turn_10.json"
        else:
            path = base / f"consequences_turn_10_window_{window}.json"

        path.write_text(json.dumps(observed, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(f"Wrote {path}")


if __name__ == "__main__":
    main()
