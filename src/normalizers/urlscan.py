import orjson as json
from pathlib import Path

def normalize_urlscan():
    """Normalize urlscan.io data."""
    raw_file = Path("data/raw/urlscan/urlscan.json")
    normalized_dir = Path("data/normalized/urlscan")
    normalized_dir.mkdir(parents=True, exist_ok=True)
    out_file = normalized_dir / "urlscan_normalized.jsonl"

    if not raw_file.exists():
        print("⚠️ urlscan.io raw data file not found. Run the collector first.")
        return

    with open(raw_file, "rb") as f:
        raw_data = json.loads(f.read())

    normalized_data = []
    for result in raw_data.get("results", []):
        normalized_data.append({
            "indicator": result.get("task", {}).get("url", "N/A"),
            "type": "url",
            "source": "urlscan.io",
            "first_seen": result.get("task", {}).get("time", "N/A"),
            "last_seen": result.get("task", {}).get("time", "N/A"),
            "tags": result.get("page", {}).get("domain", []),
        })

    with open(out_file, "wb") as f:
        for record in normalized_data:
            f.write(json.dumps(record) + b"\n")

    print(f"✅ urlscan.io data normalized and saved to {out_file}")

if __name__ == "__main__":
    normalize_urlscan()