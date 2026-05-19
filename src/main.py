from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import PlainTextResponse

from src.config import Settings, get_settings
from src.discord import (
    DiscordForwardingError,
    forward_to_discord,
)

app = FastAPI(
    title="TradingView Discord Webhook Middleware",
    description="Receives TradingView alerts and forwards them as Discord webhook messages.",
    version="1.0.0",
)


@app.get("/", response_class=PlainTextResponse)
async def root() -> str:
    return "TradingView Discord Webhook Middleware service is online"


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/webhook", response_class=PlainTextResponse)
async def webhook(
    request: Request,
    settings: Settings = Depends(get_settings),
) -> str:
    data = (await request.body()).decode("utf-8", errors="replace")

    try:
        await forward_to_discord(data, settings)
    except DiscordForwardingError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    return data
