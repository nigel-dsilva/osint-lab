import orjson as json
from pathlib import Path

def normalize_abuseipdb():
    """Normalize AbuseIPDB data."""
    raw_file = Path("data/raw/abuseipdb/abuseipdb.json")
    normalized_dir = Path("data/normalized/abuseipdb")
    normalized_dir.mkdir(parents=True, exist_ok=True)
    out_file = normalized_dir / "abuseipdb_normalized.jsonl"

    if not raw_file.exists():
        print("⚠️ AbuseIPDB raw data file not found. Run the collector first.")
        return

    with open(raw_file, "rb") as f:
        raw_data = json.loads(f.read())

    normalized_data = []
    for item in raw_data.get("data", []):
        normalized_data.append({
            "indicator": item.get("ipAddress"),
            "type": "ip",
            "source": "abuseipdb",
            "first_seen": item.get("created"),
            "last_seen": item.get("lastReportedAt"),
            "tags": [f"abuseConfidenceScore:{item.get('abuseConfidenceScore')}"],
        })

    with open(out_file, "wb") as f:
        for record in normalized_data:
            f.write(json.dumps(record) + b"\n")

    print(f"✅ AbuseIPDB data normalized and saved to {out_file}")

if __name__ == "__main__":
    normalize_abuseipdb()