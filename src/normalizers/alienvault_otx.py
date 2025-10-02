# src/normalizers/alienvault_otx.py
import orjson as json
from pathlib import Path
from datetime import datetime
from src.utils.env import load

COMMON_FIELDS = [
    "indicator", "type", "first_seen", "last_seen",
    "source", "confidence", "tags", "raw"
]

def normalize_otx(raw_path: Path, output_path: Path):
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(raw_path, "rb") as f, open(output_path, "wb") as out:
        for line in f:
            pulse = json.loads(line)
            tags = pulse.get("tags", [])
            pulse_name = pulse.get("name")
            indicators = pulse.get("indicators", [])

            for ind in indicators:
                norm = {
                    "indicator": ind.get("indicator"),
                    "type": ind.get("type"),
                    "first_seen": pulse.get("created") or ind.get("created") or datetime.utcnow().isoformat(),
                    "last_seen": pulse.get("modified") or datetime.utcnow().isoformat(),
                    "source": "alienvault_otx",
                    "confidence": 80,
                    "tags": tags + [pulse_name] if pulse_name else tags,
                    "raw": ind
                }
                for field in COMMON_FIELDS:
                    norm.setdefault(field, None)
                out.write(json.dumps(norm))
                out.write(b"\n")

if __name__ == "__main__":
    cfg = load()
    raw_dir = Path(cfg["project"]["raw_dir"]) / "alienvault_otx"
    norm_dir = Path(cfg["project"]["normalized_dir"]) / "alienvault_otx"
    norm_dir.mkdir(parents=True, exist_ok=True)

    files = sorted(raw_dir.glob("*.jsonl"))
    if not files:
        raise SystemExit("No raw alienvault_otx files found")
    raw_file = files[-1]
    out_file = norm_dir / f"{raw_file.stem}_normalized.jsonl"

    print(f"Normalizing {raw_file} -> {out_file}")
    normalize_otx(raw_file, out_file)
