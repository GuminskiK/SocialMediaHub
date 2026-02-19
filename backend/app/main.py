from fastapi import FastAPI
from app.core.config import settings
from app.core.health import check_disk, check_db, check_rss

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/health")
async def health():
    result = {"status":"ok","checks":{}}

    # Disk usage
    free_percent = check_disk()
    result["checks"]["disk"] = {"free_percent": free_percent}
    if free_percent < 10:
        result["status"] = "degraded"

    # DB Check
    db_url = settings.DATABASE_URL
    if db_url:
        
        db_ok, db_info = await check_db(settings.DATABASE_URL)
        result["checks"]["db"] = {"ok": True}
        if not db_ok:
            result["checks"]["db"] = {"ok": False, "error": db_info}
            result["status"] = "down"
    else:
        result["checks"]["db"] = {"ok": False, "error": "no DATABASE_URL"}
        result["status"] = "down"

    # RSS-Bridge check
    rss_bridge_url = settings.RSS_BRIDGE_URL
    if rss_bridge_url:
        
        rss_ok, rss_info = await check_rss(settings.RSS_BRIDGE_URL)
        result["checks"]["rss_bridge"] = {"ok": rss_info.ok, "status_code": rss_info.status_code}
        if not rss_info.ok:
            result["status"] = "degraded"
        if not rss_ok:
            result["checks"]["rss_bridge"] = {"ok": False, "error": rss_info}
            result["status"] = "degraded"

    return result