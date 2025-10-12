def score(record):
    """
    Assigns a risk score (0-100) based on multiple factors:
    - Indicator type (IP, domain, hash, etc.)
    - References count
    - ASN / Country enrichment
    - Source credibility (OTX, VirusTotal > higher weight)
    - Tags and abuse confidence scores
    """

    base = 10
    ind_type = (record.get("indicator_type") or record.get("type") or "").lower()
    refs = record.get("references", []) or []
    geo = record.get("geo", {}) or {}
    src = (record.get("source") or "").lower()
    tags = record.get("tags", []) or []
    abuse_confidence = record.get("abuseConfidenceScore", 0)

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
    if "malshare" in src:
        base += 10
    if "abuseipdb" in src:
        base += 15

    # Geo enrichment signals
    country = (geo.get("country") or "").upper()
    asn = (geo.get("asn") or "").lower()

    if country in ["RU", "CN", "IR", "KP"]:
        base += 20  # High-risk geos
    if asn and any(flag in asn for flag in ["hosting", "vpn", "tor", "cloudflare"]):
        base += 15  # Suspicious ASN types

    # Tags-based scoring
    if "malware" in tags:
        base += 30
    if "phishing" in tags:
        base += 25
    if "ransomware" in tags:
        base += 40
    if "botnet" in tags:
        base += 20

    # Abuse confidence score
    if abuse_confidence >= 90:
        base += 30
    elif abuse_confidence >= 70:
        base += 20
    elif abuse_confidence >= 50:
        base += 10

    # Cap score
    if base > 100:
        base = 100

    # Assign threat level
    if base >= 80:
        record["threat_level"] = "high"
    elif base >= 50:
        record["threat_level"] = "medium"
    else:
        record["threat_level"] = "low"

    record["score"] = base
    return record