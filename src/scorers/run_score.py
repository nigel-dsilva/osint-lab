# src/scorers/run_score.py
import orjson as json
from pathlib import Path
from src.utils.env import load
from src.scorers import simple_score

def run_score():
    cfg = load()
    merged_dir = Path(cfg['project']['merged_dir'])
    scored_dir = Path(cfg['project']['scored_dir'])
    scored_dir.mkdir(parents=True, exist_ok=True)

    in_file = merged_dir / "all.jsonl"
    out_file = scored_dir / "all_scored.jsonl"

    if not in_file.exists():
        raise SystemExit(f"No merged file found: {in_file}")

    count = 0
    with open(in_file, "rb") as inp, open(out_file, "wb") as outp:
        for line in inp:
            record = json.loads(line)

            # Normalize indicator type field
            ind_type = record.get("indicator_type") or record.get("type")
            record["indicator_type"] = ind_type

            scored = simple_score.score(record)
            outp.write(json.dumps(scored))
            outp.write(b"\n")
            count += 1

    print(f"Scored {count} records -> {out_file}")

if __name__ == "__main__":
    run_score()
