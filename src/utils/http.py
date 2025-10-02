import httpx
import backoff
from .env import load, getenv

_cfg = load()
_TIMEOUT = _cfg.get("http", {}).get("timeout_seconds", 30)
_USER_AGENT = _cfg.get("http", {}).get("user_agent", "Threat-Aggregation-Lab/1.0")

def _giveup(exc):
    return isinstance(exc, httpx.HTTPStatusError) and 400 <= exc.response.status_code < 500

@backoff.on_exception(backoff.expo, (httpx.RequestError, httpx.HTTPStatusError), max_tries=3, giveup=_giveup)
def get(url: str, params: dict | None = None, headers: dict | None = None):
    h = {"User-Agent": _USER_AGENT}
    if headers:
        h.update(headers)
    with httpx.Client(timeout=_TIMEOUT) as client:
        resp = client.get(url, params=params, headers=h)
        resp.raise_for_status()
        return resp

def auth_header_from_env(env_key: str, header_name: str = "Authorization", prefix: str = "Bearer "):
    token = getenv(env_key, "")
    return {header_name: f"{prefix}{token}"} if token else {}
