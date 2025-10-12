import orjson as json
from pathlib import Path

def normalize_malshare():
    """Normalize MalShare data."""
    raw_file = Path("data/raw/malshare/malshare.json")
    normalized_dir = Path("data/normalized/malshare")
    normalized_dir.mkdir(parents=True, exist_ok=True)
    out_file = normalized_dir / "malshare_normalized.jsonl"

    if not raw_file.exists():
        print("⚠️ MalShare raw data file not found. Run the collector first.")
        return

    with open(raw_file, "rb") as f:
        raw_data = json.loads(f.read())

    normalized_data = []
    for item in raw_data:
        normalized_data.append({
            "indicator": item.get("sha256"),
            "type": "file",
            "source": "malshare",
            "first_seen": item.get("first_seen"),
            "last_seen": item.get("last_seen"),
            "tags": item.get("tags", [])
        })

    with open(out_file, "wb") as f:
        for record in normalized_data:
            f.write(json.dumps(record) + b"\n")

    print(f"✅ MalShare data normalized and saved to {out_file}")

if __name__ == "__main__":
    normalize_malshare()