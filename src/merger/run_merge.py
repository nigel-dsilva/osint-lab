# src/merger/run_merge.py
import orjson as json
from pathlib import Path
from src.utils.env import load

def run_merge():
    cfg = load()
    enriched_dir = Path(cfg['project']['enriched_dir'])  # FIX: use enriched_dir
    merged_dir = Path(cfg['project']['merged_dir'])
    merged_dir.mkdir(parents=True, exist_ok=True)

    out_file = merged_dir / "all.jsonl"

    with open(out_file, "wb") as outp:
        count = 0
        # Loop through all enriched sources
        for source_dir in enriched_dir.rglob("*.jsonl"):
            try:
                with open(source_dir, "rb") as inp:
                    for line in inp:
                        record = json.loads(line)
                        outp.write(json.dumps(record))
                        outp.write(b"\n")
                        count += 1
            except Exception as e:
                print(f"Skipping bad file {source_dir}: {e}")

        print(f"Merged {count} records -> {out_file}")

if __name__ == "__main__":
    run_merge()
