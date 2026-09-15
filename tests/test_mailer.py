import pytest
import httpx
from fastapi import FastAPI, BackgroundTasks
from httpx import AsyncClient, ASGITransport
from fastapi_resend import ResendMailer

@pytest.fixture
def app(monkeypatch):
    fastapi_app = FastAPI()
    mailer = ResendMailer(api_key="re_test_secret_key", from_email="Support <test@resend.dev>")

    orig_post = httpx.AsyncClient.post

    async def mock_post(self, url, *args, **kwargs):
        if "api.resend.com" in str(url):
            class MockResponse:
                status_code = 200
                def json(self):
                    return {"id": "email_12345", "from": "test@resend.dev"}
            return MockResponse()
        return await orig_post(self, url, *args, **kwargs)

    monkeypatch.setattr(httpx.AsyncClient, "post", mock_post)

    @fastapi_app.post("/send")
    async def send_endpoint():
        res = await mailer.send(to="test@example.com", subject="Test", html="<p>Test</p>")
        return res

    @fastapi_app.post("/send-background")
    async def send_background_endpoint(bg: BackgroundTasks):
        mailer.send_in_background(bg, to="test@example.com", subject="Bg test", html="<p>Bg</p>")
        return {"status": "queued"}

    return fastapi_app

@pytest.mark.asyncio
async def test_resend_send(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post("/send")
        assert resp.status_code == 200
        assert resp.json()["id"] == "email_12345"

@pytest.mark.asyncio
async def test_resend_send_background(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post("/send-background")
        assert resp.status_code == 200
        assert resp.json()["status"] == "queued"
