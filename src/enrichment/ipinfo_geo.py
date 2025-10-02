import requests
import os

IPINFO_TOKEN = os.getenv("IPINFO_TOKEN")

def enrich(record):
    """
    Enrich a normalized record with IP info from ipinfo.io
    """
    ip = record.get("indicator")
    if not ip or record.get("type") != "ip":
        # Skip if no IP or not IP type
        return record

    if not IPINFO_TOKEN:
        record["geo"] = {"error": "IPINFO_TOKEN not set"}
        return record

    try:
        url = f"https://ipinfo.io/{ip}?token={IPINFO_TOKEN}"
        resp = requests.get(url, timeout=5)

        if resp.status_code != 200:
            record["geo"] = {"error": f"status {resp.status_code}"}
            return record

        data = resp.json()
        record["geo"] = {
            "ip": ip,
            "country": data.get("country"),
            "region": data.get("region"),
            "city": data.get("city"),
            "asn": data.get("org"),
        }
        return record

    except Exception as e:
        record["geo"] = {"error": str(e)}
        return record
