def score(record):
    """
    Assigns a risk score (0-100) based on multiple factors:
    - Indicator type (IP, domain, hash, etc.)
    - References count
    - ASN / Country enrichment
    - Source credibility (OTX, VirusTotal > higher weight)
    """

    base = 10
    ind_type = (record.get("indicator_type") or record.get("type") or "").lower()
    refs = record.get("references", []) or []
    geo = record.get("geo", {}) or {}
    src = (record.get("source") or "").lower()

    # Type-based scoring
    if ind_type in ["ip", "ipv4", "ipv6"]:
        base += 20
    elif ind_type in ["domain", "hostname"]:
        base += 15
    elif ind_type in ["hash", "sha256", "md5"]:
        base += 25

    # References boost
    base += min(len(refs) * 5, 20)

    # Source credibility
    if "alienvault" in src or "otx" in src:
        base += 15
    if "virustotal" in src:
        base += 20
    if "shodan" in src:
        base += 10

    # Geo enrichment signals
    country = (geo.get("country") or "").upper()
    asn = (geo.get("asn") or "").lower()

    if country in ["RU", "CN", "IR", "KP"]:
        base += 20  # High-risk geos
    if asn and any(flag in asn for flag in ["hosting", "vpn", "tor", "cloudflare"]):
        base += 15  # Suspicious ASN types

    # Cap score
    if base > 100:
        base = 100

    record["score"] = base
    return record
