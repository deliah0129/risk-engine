import argparse
import json
from pathlib import Path

from main import load_json
from phases.phase1 import run_phase1  # if this name differs, change it here

GOLDEN_DIR = Path(__file__).parent / "golden"
SESSION_PATH = Path("state/session.json")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--window", type=int, required=True)
    args = parser.parse_args()

    # Ensure golden dir exists
    GOLDEN_DIR.mkdir(parents=True, exist_ok=True)

    # Ensure session exists (Phase 0 must have been CONFIRMED)
    if not SESSION_PATH.exists():
        raise FileNotFoundError(
            f"Missing {SESSION_PATH}. Run: python main.py  -> CONFIRM (Phase 0) first."
        )

    session = load_json(SESSION_PATH)

    consequences = run_phase1(
        session=session,
        window=args.window,
        record_consequences=True,
    )

    out_path = GOLDEN_DIR / f"consequences_turn_{args.window}.json"
    out_path.write_text(json.dumps(consequences, indent=2), encoding="utf-8")

    print(f"[OK] wrote {out_path}")


if __name__ == "__main__":
    main()
