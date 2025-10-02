import orjson as json
from pathlib import Path
import sys

def pretty_print(file_path: str, limit: int = 10):
    path = Path(file_path)
    if not path.exists():
        print(f"File not found: {path}")
        return

    with open(path, "rb") as f:
        for i, line in enumerate(f, start=1):
            rec = json.loads(line)
            print(json.dumps(rec, option=json.OPT_INDENT_2).decode())
            print("-" * 60)
            if i >= limit:
                break

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m src.reporting.json_pp <file_path> [limit]")
        sys.exit(1)

    file_path = sys.argv[1]
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    pretty_print(file_path, limit)
