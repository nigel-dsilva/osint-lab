import requests
from pathlib import Path
from src.utils.env import load
import orjson as json

def collect_urlscan():
    """Collect data from the urlscan.io API."""
    cfg = load()
    api_key = "0199cf62-dc8e-7448-ad60-a8fa9d23353f"
    if not api_key:
        print("⚠️ urlscan.io API key is missing. Add it to your .env file.")
        return

    url = "https://urlscan.io/api/v1/search/"
    headers = {
        "API-Key": api_key,
        "User-Agent": cfg.get("GENERIC_USER_AGENT", "ThreatIntel-Lab/1.0"),
    }

    # Example query: Fetch recent scans
    params = {"q": "domain:example.com"}  # Replace with your query
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        print(f"⚠️ Failed to fetch data from urlscan.io. HTTP {response.status_code}: {response.text}")
        return

    raw_data = response.json()
    raw_dir = Path("data/raw/urlscan")
    raw_dir.mkdir(parents=True, exist_ok=True)
    out_file = raw_dir / "urlscan.json"

    with open(out_file, "wb") as f:
        f.write(json.dumps(raw_data))

    print(f"✅ urlscan.io data collected and saved to {out_file}")

if __name__ == "__main__":
    collect_urlscan()