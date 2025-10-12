from src.utils.env import load
from src.collectors.base_generic import collect_source
from src.collectors.malshare import collect_malshare
from src.collectors.abuseipdb import collect_abuseipdb
from src.collectors.urlscan import collect_urlscan
from src.collectors.securitytrails import collect_securitytrails

def run_all():
    collect_malshare()
    collect_abuseipdb()
    collect_urlscan()
    collect_securitytrails()  
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
