import orjson as json
from pathlib import Path

def normalize_securitytrails():
    """Normalize SecurityTrails data."""
    raw_file = Path("data/raw/securitytrails/securitytrails.json")
    normalized_dir = Path("data/normalized/securitytrails")
    normalized_dir.mkdir(parents=True, exist_ok=True)
    out_file = normalized_dir / "securitytrails_normalized.jsonl"

    if not raw_file.exists():
        print("⚠️ SecurityTrails raw data file not found. Run the collector first.")
        return

    with open(raw_file, "rb") as f:
        raw_data = json.loads(f.read())

    normalized_data = []
    for subdomain in raw_data.get("subdomains", []):
        normalized_data.append({
            "indicator": f"{subdomain}.example.com",
            "type": "domain",
            "source": "securitytrails",
            "tags": ["subdomain"],
        })

    with open(out_file, "wb") as f:
        for record in normalized_data:
            f.write(json.dumps(record) + b"\n")

    print(f"✅ SecurityTrails data normalized and saved to {out_file}")

if __name__ == "__main__":
    normalize_securitytrails()