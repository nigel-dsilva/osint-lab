import requests
from pathlib import Path
from src.utils.env import load
import orjson as json

def collect_securitytrails():
    """Collect data from the SecurityTrails API."""
    cfg = load()
    api_key = "j1roLMAxmrq_1NWW27hcncWR8XvlX6z0"
    if not api_key:
        print("⚠️ SecurityTrails API key is missing. Add it to your .env file.")
        return

    url = "https://api.securitytrails.com/v1/domain/example.com/subdomains"
    headers = {
        "APIKEY": api_key,
        "User-Agent": cfg.get("GENERIC_USER_AGENT", "ThreatIntel-Lab/1.0"),
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"⚠️ Failed to fetch data from SecurityTrails. HTTP {response.status_code}: {response.text}")
        return

    raw_data = response.json()
    raw_dir = Path("data/raw/securitytrails")
    raw_dir.mkdir(parents=True, exist_ok=True)
    out_file = raw_dir / "securitytrails.json"

    with open(out_file, "wb") as f:
        f.write(json.dumps(raw_data))

    print(f"✅ SecurityTrails data collected and saved to {out_file}")

if __name__ == "__main__":
    collect_securitytrails()