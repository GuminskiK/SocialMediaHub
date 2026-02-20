from fastapi import FastAPI
from app.core.config import settings
from app.core.health import check_disk, check_db, check_rss

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/health")
async def health():
    result = {"status": "ok", "checks": {}}

    # Disk usage
    disk_ok, disk_info = check_disk()
    result["checks"]["disk"] = disk_info
    if not disk_ok:
        result["status"] = "degraded"

    # DB Check
    db_url = settings.DATABASE_URL
    if db_url:
        db_ok, db_info = await check_db(db_url)
        result["checks"]["db"] = {"ok": db_ok, "info": db_info}
        if not db_ok:
            result["status"] = "down"
    else:
        result["checks"]["db"] = {"ok": False, "error": "no DATABASE_URL"}
        result["status"] = "down"

    # RSS-Bridge check
    rss_bridge_url = settings.RSS_BRIDGE_URL
    if rss_bridge_url:
        rss_ok, rss_info = await check_rss(rss_bridge_url)
        result["checks"]["rss_bridge"] = {"ok": rss_ok, "info": rss_info}
        if not rss_ok and result["status"] != "down":
            result["status"] = "degraded"

    return result