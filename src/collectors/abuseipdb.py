import requests
from pathlib import Path
from src.utils.env import load
import orjson as json

def collect_abuseipdb():
    """Collect data from the AbuseIPDB API."""
    cfg = load()
    api_key = "c059db5442117521958ceddebb9d319d1e8bdc7d5cb81badb69715adab3318cbd611ec4006bcde22"
    if not api_key:
        print("⚠️ AbuseIPDB API key is missing. Add it to your .env file.")
        return

    url = "https://api.abuseipdb.com/api/v2/blacklist"
    headers = {
        "Key": api_key,
        "Accept": "application/json",
        "User-Agent": cfg.get("GENERIC_USER_AGENT", "ThreatIntel-Lab/1.0"),
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"⚠️ Failed to fetch data from AbuseIPDB. HTTP {response.status_code}: {response.text}")
        return

    raw_data = response.json()
    raw_dir = Path("data/raw/abuseipdb")
    raw_dir.mkdir(parents=True, exist_ok=True)
    out_file = raw_dir / "abuseipdb.json"

    with open(out_file, "wb") as f:
        f.write(json.dumps(raw_data))

    print(f"✅ AbuseIPDB data collected and saved to {out_file}")

if __name__ == "__main__":
    collect_abuseipdb()