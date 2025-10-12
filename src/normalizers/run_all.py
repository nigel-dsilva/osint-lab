"""
Run all normalizers: OTX, VirusTotal, Shodan, GreyNoise
"""

import subprocess
from src.normalizers.malshare import normalize_malshare
from src.normalizers.abuseipdb import normalize_abuseipdb
from src.normalizers.urlscan import normalize_urlscan
from src.normalizers.securitytrails import normalize_securitytrails

NORMALIZERS = [
    ["python", "-m", "src.normalizers.alienvault_otx"],
    ["python", "-m", "src.normalizers.virustotal"],
    ["python", "-m", "src.normalizers.shodan"],
    ["python", "-m", "src.normalizers.greynoise"]
]

def run_all():
    normalize_malshare()
    normalize_abuseipdb()
    normalize_urlscan()
    normalize_securitytrails()
    for norm in NORMALIZERS:
        print("\n--- Running:", " ".join(norm))
        subprocess.run(norm, check=True)

if __name__ == "__main__":
    run_all()
