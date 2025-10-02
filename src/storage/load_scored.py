import orjson as json
from pathlib import Path
from datetime import datetime, timezone
from src.utils.env import load
from src.storage import db

def load_scored():
    cfg = load()
    scored_dir = Path(cfg['project']['scored_dir'])

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    in_file = scored_dir / f"{stamp}.jsonl"

    if not in_file.exists():
        raise SystemExit(f"No scored file found: {in_file}")

    db.init_db()
    records = []
    with open(in_file, "rb") as inp:
        for line in inp:
            rec = json.loads(line)
            records.append((
                rec.get("indicator"),
                rec.get("indicator_type"),
                rec.get("first_seen"),
                rec.get("last_seen"),
                rec.get("source"),
                rec.get("confidence"),
                rec.get("score"),
                rec.get("geo", {}).get("country"),
                rec.get("geo", {}).get("asn")
            ))

    db.insert_many(records)
    print(f"Inserted {len(records)} records into database.")

if __name__ == "__main__":
    load_scored()
