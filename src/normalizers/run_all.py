"""
Run all normalizers: OTX, VirusTotal, Shodan, GreyNoise
"""

import subprocess

NORMALIZERS = [
    ["python", "-m", "src.normalizers.alienvault_otx"],
    ["python", "-m", "src.normalizers.virustotal"],
    ["python", "-m", "src.normalizers.shodan"],
    ["python", "-m", "src.normalizers.greynoise"]
]

def run_all():
    for norm in NORMALIZERS:
        print("\n--- Running:", " ".join(norm))
        subprocess.run(norm, check=True)

if __name__ == "__main__":
    run_all()
