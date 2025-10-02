# src/normalizers/run_normalise.py
import orjson as json
from pathlib import Path
from src.utils.env import load

# Import each normalizer
from src.normalizers.alienvault_otx import normalize_otx
from src.normalizers.virustotal import normalize_virustotal
from src.normalizers.shodan import normalize_shodan
from src.normalizers.greynoise import normalize_greynoise

# Map source → function
NORMALIZERS = {
    "alienvault_otx": normalize_otx,
    "virustotal": normalize_virustotal,
    "shodan": normalize_shodan,
    "greynoise": normalize_greynoise,
}

def normalize_all():
    cfg = load()
    raw_dir = Path(cfg['project']['raw_dir'])
    normalized_dir = Path(cfg['project']['normalized_dir'])

    for source_dir in raw_dir.iterdir():
        if not source_dir.is_dir():
            continue

        normalizer = NORMALIZERS.get(source_dir.name)
        if not normalizer:
            print(f"⚠️ No normalizer for {source_dir.name}, skipping.")
            continue

        for f in sorted(source_dir.glob("*.jsonl")):
            out_dir = normalized_dir / source_dir.name
            out_dir.mkdir(parents=True, exist_ok=True)
            out_file = out_dir / f.name.replace(".jsonl", "_normalized.jsonl")

            print(f"Normalizing {f} with {normalizer.__name__} -> {out_file}")
            normalizer(f, out_file)

if __name__ == "__main__":
    normalize_all()
