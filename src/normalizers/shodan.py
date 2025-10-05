def collect_shodan():
    """Collect data from Shodan"""
    base_url = "https://api.shodan.io"
    headers = {"Accept": "application/json"}
    ips = ["8.8.8.8", "1.1.1.1", "4.2.2.2"]
    results = []

    for ip in ips:
        url = f"{base_url}/shodan/host/{ip}?key={SHODAN_API_KEY}"
        r = requests.get(url, headers=headers, timeout=20)
        if r.status_code == 200:
            data = r.json()
            results.append({
                "ip": data.get("ip_str", ip),
                "ports": data.get("ports", []),
                "org": data.get("org", ""),
                "asn": data.get("asn", ""),
                "country": data.get("country_name", ""),
                "last_update": data.get("last_update", datetime.now(timezone.utc).isoformat()),
                "source": "shodan"
            })
        else:
            print(f"⚠️ Skipped {ip} (HTTP {r.status_code})")

    return save_jsonl(results, "shodan")