import argparse
import json
from pathlib import Path

from main import load_json
from phases.phase2 import run_phase_2

# Paths
REPO_ROOT = Path(__file__).resolve().parents[2]
GOLDEN_DIR = Path(__file__).parent
SESSION_PATH = REPO_ROOT / "state" / "session.json"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--window", type=int, required=True)
    args = parser.parse_args()

    if not SESSION_PATH.exists():
        raise FileNotFoundError(
            f"Missing {SESSION_PATH}. Run main.py first and CONFIRM Phase 0."
        )

    session = load_json(SESSION_PATH)

    consequences = run_phase_2(
        session=session,
        window=args.window,
        record_consequences=True,
    )

    out_path = GOLDEN_DIR / f"consequences_turn_{args.window}.json"
    out_path.write_text(json.dumps(consequences, indent=2), encoding="utf-8")

    print(f"[OK] wrote {out_path}")


if __name__ == "__main__":
    main()
