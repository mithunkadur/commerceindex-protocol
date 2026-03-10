"""CommerceIndex SDK — Real-time commerce feed."""

from __future__ import annotations

import asyncio
import json
from typing import AsyncIterator, TYPE_CHECKING

from commerceindex.models import CommerceEvent

if TYPE_CHECKING:
    from commerceindex.client import CommerceIndex


class FeedClient:
    """Real-time commerce feed operations."""

    def __init__(self, client: CommerceIndex):
        self._client = client

    async def latest(self) -> list[CommerceEvent]:
        """Get latest commerce events via REST."""
        data = await self._client._request("GET", "/v1/feed")
        return [CommerceEvent(**e) for e in data.get("events", [])]

    async def stream(
        self,
        channels: list[str] | None = None,
        reconnect: bool = True,
        max_reconnect_delay: float = 30.0,
    ) -> AsyncIterator[CommerceEvent]:
        """Stream commerce events via WebSocket.

        Args:
            channels: Channels to subscribe to (e.g., ["tasks:new", "deals:closed"]).
                      If None, receives all events.
            reconnect: Auto-reconnect on disconnect.
            max_reconnect_delay: Maximum delay between reconnection attempts.

        Yields:
            CommerceEvent objects as they arrive.
        """
        try:
            import websockets
        except ImportError:
            raise ImportError(
                "websockets package required for streaming. "
                "Install with: pip install commerceindex[websockets] or pip install websockets"
            )

        ws_url = self._client._base_url.replace("https://", "wss://").replace(
            "http://", "ws://"
        )
        ws_url = f"{ws_url}/v1/gateway/ws?token={self._client._api_key}"

        delay = 1.0
        while True:
            try:
                async with websockets.connect(ws_url) as ws:
                    delay = 1.0  # Reset on successful connect

                    # Subscribe to channels
                    if channels:
                        await ws.send(
                            json.dumps({"action": "subscribe", "channels": channels})
                        )

                    async for message in ws:
                        try:
                            data = json.loads(message)
                            if "event_type" in data or "event_id" in data:
                                yield CommerceEvent(**data)
                        except (json.JSONDecodeError, Exception):
                            continue

            except Exception:
                if not reconnect:
                    break
                await asyncio.sleep(delay)
                delay = min(delay * 2, max_reconnect_delay)

    async def stream_sse(self) -> AsyncIterator[CommerceEvent]:
        """Stream commerce events via Server-Sent Events (fallback).

        Yields:
            CommerceEvent objects as they arrive.
        """
        async with self._client._http.stream(
            "GET", "/v1/gateway/events"
        ) as response:
            buffer = ""
            async for chunk in response.aiter_text():
                buffer += chunk
                while "\n\n" in buffer:
                    event_str, buffer = buffer.split("\n\n", 1)
                    data_line = None
                    for line in event_str.split("\n"):
                        if line.startswith("data: "):
                            data_line = line[6:]
                    if data_line:
                        try:
                            data = json.loads(data_line)
                            yield CommerceEvent(**data)
                        except (json.JSONDecodeError, Exception):
                            continue
