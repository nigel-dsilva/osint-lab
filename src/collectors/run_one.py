from src.utils.env import load
from src.collectors.base_generic import collect_source

def run(key: str):
    cfg = load()
    sources = cfg.get("sources", [])
    s = next((x for x in sources if x.get("key") == key and x.get("enabled")), None)
    if not s:
        raise SystemExit(f"source '{key}' not found or not enabled in config/config.yaml")
    path = collect_source(s)
    print("Wrote raw file:", path)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        raise SystemExit("usage: python -m src.collectors.run_one <source_key>")
    run(sys.argv[1])
