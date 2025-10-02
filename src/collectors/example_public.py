from pathlib import Path
from datetime import datetime, timezone
import orjson as json
from src.utils.env import load
from src.utils import http

def run():
    cfg = load()
    url = "https://httpbin.org/json"
    r = http.get(url)
    data = r.json()

    out_dir = Path(cfg["project"]["raw_dir"]) / "example_public"
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    out_file = out_dir / f"{stamp}.jsonl"

    with open(out_file, "ab") as f:
        f.write(json.dumps(data))
        f.write(b"\n")

    print("WROTE:", out_file)
    return str(out_file)

if __name__ == "__main__":
    run()
