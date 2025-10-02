import random
from typing import Dict, Any

def enrich(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Fake enrichment: attaches a random country & ASN.
    Later this will be replaced with real services.
    """
    countries = ["US", "IN", "DE", "BR", "FR", "SG"]
    asns = ["AS13335", "AS15169", "AS8075", "AS32934"]

    record["geo"] = {
        "country": random.choice(countries),
        "asn": random.choice(asns)
    }
    return record
