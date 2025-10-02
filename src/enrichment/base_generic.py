# src/enrichment/base_generic.py
import orjson as json
from pathlib import Path

def enrich_file(input_file: Path, enricher_func, enricher_name: str, enriched_dir: Path) -> Path:
    """
    Apply an enricher function to each record in a normalized file.
    Writes output into enriched_dir/<enricher_name>/<relative_path>.jsonl
    """
    rel = input_file.relative_to(input_file.parents[1])
    out_file = enriched_dir / enricher_name / rel
    out_file.parent.mkdir(parents=True, exist_ok=True)

    with open(input_file, "rb") as inp, open(out_file, "wb") as outp:
        for line in inp:
            try:
                record = json.loads(line)
                enriched = enricher_func(record)
                outp.write(json.dumps(enriched))
                outp.write(b"\n")
            except Exception as e:
                print(f"[WARN] Skipping bad record in {input_file}: {e}")

    return out_file
