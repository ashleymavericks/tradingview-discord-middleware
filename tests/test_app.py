from fastapi.testclient import TestClient

from src.config import Settings
from src.main import app, get_settings


def test_root() -> None:
    client = TestClient(app)

    response = client.get("/")

    assert response.status_code == 200
    assert response.text == "TradingView Discord Webhook Middleware service is online"


def test_health() -> None:
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_webhook_forwards_raw_body(monkeypatch) -> None:
    forwarded: list[tuple[str, Settings]] = []

    async def fake_forward_to_discord(message: str, settings: Settings) -> None:
        forwarded.append((message, settings))

    app.dependency_overrides[get_settings] = lambda: Settings(
        DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/example/token"
    )
    monkeypatch.setattr(
        "src.main.forward_to_discord",
        fake_forward_to_discord,
    )
    client = TestClient(app)

    response = client.post("/webhook", content="BTCUSD crossed 70000")

    assert response.status_code == 200
    assert response.text == "BTCUSD crossed 70000"
    assert forwarded[0][0] == "BTCUSD crossed 70000"

    app.dependency_overrides.clear()
