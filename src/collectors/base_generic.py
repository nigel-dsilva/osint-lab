from __future__ import annotations
from pathlib import Path
from datetime import datetime, timedelta, timezone
import time, orjson as json
from typing import Dict, Iterable, Any, Optional
import os

from src.utils.env import load
from src.utils import http
from .state import load as load_state, save as save_state


def _iso_days_ago(days: int) -> str:
    dt = datetime.now(timezone.utc) - timedelta(days=days)
    return dt.isoformat()


def _sleep_for_rl(req_per_min: Optional[int]):
    if req_per_min and req_per_min > 0:
        time.sleep(60.0 / float(req_per_min))


def _write_jsonl(path: Path, items: Iterable[Any]):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "ab") as f:
        for it in items:
            f.write(json.dumps(it))
            f.write(b"\n")


def collect_source(source_cfg: Dict[str, Any]) -> str:
    cfg = load()
    raw_dir = Path(cfg["project"]["raw_dir"])
    out_dir = raw_dir / source_cfg["key"]
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    out_file = out_dir / f"{stamp}.jsonl"

    base_url = source_cfg.get("base_url", "").rstrip("/")
    rl = source_cfg.get("rate_limit", {}).get("req_per_min", None)

    for ep in source_cfg.get("endpoints", []):
        params = {}
        headers = {}
        p = ep.get("params", {}) or {}
        limit_param = p.get("limit_param")
        page_param = p.get("page_param")
        cursor_param = p.get("cursor_param")
        date_param = p.get("date_param")
        default_limit = p.get("default_limit", 200)
        lookback_days = p.get("default_lookback_days", 7)

        if limit_param:
            params[limit_param] = default_limit
        if date_param:
            params[date_param] = _iso_days_ago(lookback_days)

        # auth
        if source_cfg.get("auth_type") == "header":
            headers.update(http.auth_header_from_env(source_cfg.get("auth_env_key", "")))
        elif source_cfg.get("auth_type") == "query":
            tok = os.getenv(source_cfg.get("auth_env_key", ""), "")
            if tok:
                params["api_key"] = tok

        url = f"{base_url}{ep['path']}"
        page = 1
        cursor = None
        seen = set()

        while True:
            run_params = dict(params)
            if page_param:
                run_params[page_param] = page
            if cursor_param and cursor:
                run_params[cursor_param] = cursor

            resp = http.get(url, params=run_params, headers={**source_cfg.get("headers", {}), **headers})
            data = resp.json()

            if isinstance(data, list):
                items = data
            elif isinstance(data, dict):
                items = data.get("items") or data.get("results") or data.get("data") or [data]
                if not isinstance(items, list):
                    items = [data]
            else:
                items = [data]

            # ✅ dedupe with large integer fix
            uniq = []
            for it in items:
                try:
                    # strict integer mode (will fail if >64-bit)
                    b = json.dumps(it, option=json.OPT_STRICT_INTEGER)
                except Exception:
                    # fallback: stringify huge ints
                    safe_it = {
                        k: (str(v) if isinstance(v, int) and abs(v) > 2**63 else v)
                        for k, v in it.items()
                    }
                    b = json.dumps(safe_it)
                    it = safe_it  # only overwrite if fallback was used
                if b not in seen:
                    seen.add(b)
                    uniq.append(it)

            if uniq:
                _write_jsonl(out_file, uniq)

            # pagination
            next_cursor = None
            if cursor_param and isinstance(data, dict):
                next_cursor = data.get("next_cursor") or data.get("next") or data.get("cursor")
            more_by_page = bool(page_param and len(items) == default_limit)
            more_by_cursor = bool(cursor_param and next_cursor)
            if not (more_by_page or more_by_cursor):
                break

            cursor = next_cursor if next_cursor else cursor
            page += 1
            _sleep_for_rl(rl)

    return str(out_file)
