import asyncpg
import httpx
import shutil
import os

def check_disk():
    total, used, free = shutil.disk_usage(os.path.absolutepath(os.sep))
    free_percent = round( free / total * 100, 2)
    return free_percent

async def check_db(url: str, timeout: int = 3):
    try:
        conn = await asyncpg.connect(dsn=url, timeout=timeout)
        await conn.fetchval("SELECT 1")
        await conn.close()
        return True, None
    except Exception as e:
        return False, str(e)

async def check_rss(url: str, timeout: int = 4):
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            r = await client.get(url)
            return True, r.status_code
    except Exception as e:
        return False, str(e)