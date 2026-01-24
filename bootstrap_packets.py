from pathlib import Path

ROOT = Path(__file__).parent

STRUCTURE = {
    "packets": {
        "README.md": "",
        "smoke": {
            "README.md": "",
            "run.bat": "",
            "run.sh": "",
        },
        "determinism": {
            "README.md": "",
            "run.bat": "",
            "run.sh": "",
        },
        "contract": {
            "README.md": "",
            "run.bat": "",
            "run.sh": "",
        },
    },
    "scripts": {
        "packet_common.py": "",
        "packet_smoke.py": "",
        "packet_determinism.py": "",
        "packet_contract.py": "",
    },
}


def create_tree(base: Path, tree: dict):
    for name, content in tree.items():
        path = base / name
        if isinstance(content, dict):
            path.mkdir(parents=True, exist_ok=True)
            create_tree(path, content)
        else:
            if not path.exists():
                path.write_text(content, encoding="utf-8")


if __name__ == "__main__":
    create_tree(ROOT, STRUCTURE)
    print("OK: testing packet folders created")
