# src/normalizers/virustotal.py
import orjson as json
from pathlib import Path
from datetime import datetime
from src.utils.env import load

COMMON_FIELDS = [
    "indicator", "type", "first_seen", "last_seen",
    "source", "confidence", "tags", "raw"
]

def normalize_virustotal(raw_path: Path, output_path: Path):
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(raw_path, "rb") as f, open(output_path, "wb") as out:
        for line in f:
            raw_json = json.loads(line)
            data = raw_json.get("data", {})

            ind = data.get("id")
            ind_type = data.get("type")
            attributes = data.get("attributes", {})

            norm = {
                "indicator": ind,
                "type": ind_type,
                "first_seen": attributes.get("first_submission_date") or datetime.utcnow().isoformat(),
                "last_seen": attributes.get("last_analysis_date") or datetime.utcnow().isoformat(),
                "source": "virustotal",
                "confidence": 85,
                "tags": list(attributes.get("categories", {}).keys()) if "categories" in attributes else [],
                "raw": data
            }
            for field in COMMON_FIELDS:
                norm.setdefault(field, None)
            out.write(json.dumps(norm))
            out.write(b"\n")

if __name__ == "__main__":
    cfg = load()
    raw_dir = Path(cfg["project"]["raw_dir"]) / "virustotal"
    norm_dir = Path(cfg["project"]["normalized_dir"]) / "virustotal"
    norm_dir.mkdir(parents=True, exist_ok=True)

    files = sorted(raw_dir.glob("*.jsonl"))
    if not files:
        raise SystemExit("No raw virustotal files found")
    raw_file = files[-1]
    out_file = norm_dir / f"{raw_file.stem}_normalized.jsonl"

    print(f"Normalizing {raw_file} -> {out_file}")
    normalize_virustotal(raw_file, out_file)
