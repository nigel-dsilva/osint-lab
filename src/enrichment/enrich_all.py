# src/enrichment/enrich_all.py
from pathlib import Path
from src.utils.env import load
from src.enrichment.base_generic import enrich_file
from src.enrichment import dummy_geo, ipinfo_geo

# Register enrichers
ENRICHERS = {
    "dummy_geo": dummy_geo.enrich,
    "ipinfo_geo": ipinfo_geo.enrich,
}

def run_all():
    cfg = load()

    normalized_dir = Path(cfg['project']['normalized_dir'])
    enriched_dir = Path(cfg['project']['enriched_dir'])
    enriched_dir.mkdir(parents=True, exist_ok=True)

    for source_dir in normalized_dir.iterdir():
        if not source_dir.is_dir():
            continue

        for f in sorted(source_dir.glob("*.jsonl")):
            for name, func in ENRICHERS.items():
                print(f"Enriching: {f} with {name}")
                out = enrich_file(f, func, name, enriched_dir)
                print("  ->", out)

if __name__ == "__main__":
    run_all()
