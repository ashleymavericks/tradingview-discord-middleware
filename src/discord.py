import httpx

from src.config import Settings


class DiscordForwardingError(RuntimeError):
    """Raised when Discord rejects or cannot receive the forwarded alert."""


async def forward_to_discord(message: str, settings: Settings) -> None:
    if settings.discord_webhook_url is None:
        raise DiscordForwardingError("DISCORD_WEBHOOK_URL is not configured")

    payload = {"content": message}
    try:
        async with httpx.AsyncClient(timeout=settings.discord_timeout_seconds) as client:
            response = await client.post(str(settings.discord_webhook_url), json=payload)
            response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        status_code = exc.response.status_code
        raise DiscordForwardingError(
            f"Discord webhook returned HTTP {status_code}"
        ) from exc
    except httpx.HTTPError as exc:
        raise DiscordForwardingError("Discord webhook request failed") from exc
