import requests
from pathlib import Path
from src.utils.env import load
import orjson as json

def collect_malshare():
    """Collect data from the MalShare API."""
    cfg = load()
    api_key = "3302bf44a560f7d8d0055446d1660aa13f7bbb17282ae44a33186daef04e4e73"
    if not api_key:
        print("⚠️ MalShare API key is missing. Add it to your .env file.")
        return

    url = f"https://malshare.com/api.php?api_key={api_key}&action=getlist"
    headers = {"User-Agent": cfg.get("GENERIC_USER_AGENT", "ThreatIntel-Lab/1.0")}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"⚠️ Failed to fetch data from MalShare. HTTP {response.status_code}: {response.text}")
        return

    raw_data = response.json()
    raw_dir = Path("data/raw/malshare")
    raw_dir.mkdir(parents=True, exist_ok=True)
    out_file = raw_dir / "malshare.json"

    with open(out_file, "wb") as f:
        f.write(json.dumps(raw_data))

    print(f"✅ MalShare data collected and saved to {out_file}")

if __name__ == "__main__":
    collect_malshare()