from typing import Any, Dict
from datetime import datetime, timezone

def to_stix_like(raw: Dict[str, Any], source: str) -> Dict[str, Any]:
    """
    Convert a raw record into a STIX-like normalized format.
    """
    now = datetime.now(timezone.utc).isoformat()

    return {
        "indicator": raw.get("indicator")
            or raw.get("ioc")
            or raw.get("value")
            or raw.get("url")
            or raw.get("ip")
            or "",
        "indicator_type": raw.get("type")
            or raw.get("ioc_type")
            or raw.get("category")
            or "unknown",
        "first_seen": raw.get("first_seen") or raw.get("created") or now,
        "last_seen": raw.get("last_seen") or raw.get("updated") or now,
        "source": source,
        "confidence": raw.get("confidence") or raw.get("score") or "medium",
        "references": raw.get("references") or raw.get("links") or [],
    }
