# src/normalizers/greynoise.py
import orjson as json
from pathlib import Path
from datetime import datetime
from src.utils.env import load

COMMON_FIELDS = [
    "indicator", "type", "first_seen", "last_seen",
    "source", "confidence", "tags", "raw"
]

def normalize_greynoise(raw_path: Path, output_path: Path):
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(raw_path, "rb") as f, open(output_path, "wb") as out:
        for line in f:
            raw_json = json.loads(line)
            ip = raw_json.get("ip")
            classification = raw_json.get("classification")
            name = raw_json.get("name")
            seen = raw_json.get("seen", False)
            tags = []
            if classification: tags.append(f"class:{classification}")
            if name: tags.append(f"name:{name}")
            if seen: tags.append("seen:true")

            norm = {
                "indicator": ip,
                "type": "ip",
                "first_seen": raw_json.get("first_seen") or datetime.utcnow().isoformat(),
                "last_seen": raw_json.get("last_seen") or datetime.utcnow().isoformat(),
                "source": "greynoise",
                "confidence": 75 if classification == "benign" else 90,
                "tags": tags,
                "raw": raw_json
            }
            for field in COMMON_FIELDS:
                norm.setdefault(field, None)
            out.write(json.dumps(norm))
            out.write(b"\n")

if __name__ == "__main__":
    cfg = load()
    raw_dir = Path(cfg["project"]["raw_dir"]) / "greynoise"
    norm_dir = Path(cfg["project"]["normalized_dir"]) / "greynoise"
    norm_dir.mkdir(parents=True, exist_ok=True)

    files = sorted(raw_dir.glob("*.jsonl"))
    if not files:
        raise SystemExit("No raw greynoise files found")
    raw_file = files[-1]
    out_file = norm_dir / f"{raw_file.stem}_normalized.jsonl"

    print(f"Normalizing {raw_file} -> {out_file}")
    normalize_greynoise(raw_file, out_file)
