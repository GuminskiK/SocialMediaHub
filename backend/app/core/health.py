import asyncpg
import httpx
import shutil
import os
from typing import Tuple, Any


def check_disk(min_free_percent: float = 10.0) -> Tuple[bool, dict]:
    """Return (ok, info) for disk usage check."""
    total, used, free = shutil.disk_usage(os.path.abspath(os.sep))
    free_pct = round(free / total * 100, 2)
    ok = free_pct >= min_free_percent
    return ok, {"free_percent": free_pct}


async def check_db(url: str, timeout: int = 3) -> Tuple[bool, Any]:
    try:
        conn = await asyncpg.connect(dsn=url, timeout=timeout)
        await conn.fetchval("SELECT 1")
        await conn.close()
        return True, None
    except Exception as e:
        return False, str(e)


async def check_rss(url: str | None, timeout: int = 4) -> Tuple[bool, Any]:
    """Return (ok, info) for RSS-Bridge URL check using httpx async client."""
    if not url:
        return False, "no_url"
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            resp = await client.get(url)
            ok = 200 <= resp.status_code < 400
            return ok, {"status_code": resp.status_code}
    except Exception as e:
        return False, str(e)