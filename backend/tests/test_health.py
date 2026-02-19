import pytest
import respx
from httpx import Response
from app.core.health import check_disk, check_db, check_rss


def test_check_disk_always_returns_free_percent():
    ok, info = check_disk(min_free_percent=0)
    assert "free_percent" in info
    assert isinstance(info["free_percent"], float)
    assert ok is True


@respx.mock
@pytest.mark.asyncio
async def test_check_rss_ok():
    url = "http://rss_bridge:80"
    respx.get(url).mock(return_value=Response(200))
    ok, info = await check_rss(url)
    assert ok is True
    assert info["status_code"] == 200


@respx.mock
@pytest.mark.asyncio
async def test_check_rss_not_found():
    url = "http://rss_bridge:80/notfound"
    respx.get(url).mock(return_value=Response(404))
    ok, info = await check_rss(url)
    assert ok is False
    assert info["status_code"] == 404
