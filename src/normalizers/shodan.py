# src/normalizers/shodan.py
import json
from pathlib import Path
from datetime import datetime

COMMON_FIELDS = [
    "indicator", "type", "first_seen", "last_seen",
    "source", "confidence", "tags", "raw"
]

def normalize_shodan(raw_path: Path, output_path: Path):
    """
    Normalize Shodan host lookup data into common schema.
    Free API returns metadata about a single IP.
    """

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(raw_path, "r", encoding="utf-8") as f:
        raw_json = json.load(f)

    ip = raw_json.get("ip_str")
    org = raw_json.get("org")
    os = raw_json.get("os")
    tags = []

    if org:
        tags.append(f"org:{org}")
    if os:
        tags.append(f"os:{os}")

    # services data
    services = raw_json.get("data", [])

    with open(output_path, "w", encoding="utf-8") as out:
        for svc in services:
            port = svc.get("port")
            proto = svc.get("transport")
            product = svc.get("product")

            record_tags = tags.copy()
            if port:
                record_tags.append(f"port:{port}")
            if proto:
                record_tags.append(f"proto:{proto}")
            if product:
                record_tags.append(f"product:{product}")

            norm = {
                "indicator": ip,
                "type": "ip",
                "first_seen": svc.get("timestamp") or datetime.utcnow().isoformat(),
                "last_seen": datetime.utcnow().isoformat(),
                "source": "shodan",
                "confidence": 80,  # Free API host lookup
                "tags": record_tags,
                "raw": svc
            }

            for field in COMMON_FIELDS:
                norm.setdefault(field, None)

            out.write(json.dumps(norm) + "\n")


if __name__ == "__main__":
    raw_file = Path("data/raw/shodan/sample.json")
    out_file = Path("data/normalized/shodan/sample.jsonl")
    normalize_shodan(raw_file, out_file)
    print(f"Normalized data written to {out_file}")
