from src.utils.env import load
from src.collectors.base_generic import collect_source

def run_all():
    cfg = load()
    sources = cfg.get("sources", [])
    for s in sources:
        if s.get("enabled"):
            print("Collecting:", s["key"])
            try:
                path = collect_source(s)
                print("  ->", path)
            except Exception as e:
                print("  ERROR collecting", s["key"], e)

if __name__ == "__main__":
    run_all()
