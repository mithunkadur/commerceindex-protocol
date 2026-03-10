/** CommerceIndex SDK — Real-time commerce feed. */

import type { CommerceIndex } from "./client.js";
import type { CommerceEvent } from "./types.js";

export class FeedClient {
  constructor(private client: CommerceIndex) {}

  /** Get latest commerce events via REST. */
  async latest(): Promise<CommerceEvent[]> {
    const data = await this.client._request<{ events: CommerceEvent[] }>("GET", "/v1/feed");
    return data.events;
  }

  /**
   * Stream commerce events via WebSocket.
   *
   * Requires a WebSocket implementation (native in Node 22+, or use 'ws' package).
   *
   * @param channels - Channels to subscribe to (e.g., ["tasks:new", "deals:closed"])
   * @param onEvent - Callback for each received event
   * @param onError - Error callback
   * @returns Cleanup function to close the connection
   */
  stream(
    channels: string[],
    onEvent: (event: CommerceEvent) => void,
    onError?: (error: Error) => void
  ): () => void {
    const baseUrl = this.client.getBaseUrl();
    const apiKey = this.client.getApiKey();
    const wsUrl = baseUrl
      .replace("https://", "wss://")
      .replace("http://", "ws://");

    let ws: WebSocket | null = null;
    let closed = false;
    let reconnectDelay = 1000;

    const connect = () => {
      if (closed) return;

      try {
        ws = new WebSocket(`${wsUrl}/v1/gateway/ws?token=${apiKey}`);

        ws.onopen = () => {
          reconnectDelay = 1000;
          if (channels.length > 0) {
            ws!.send(JSON.stringify({ action: "subscribe", channels }));
          }
        };

        ws.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data as string);
            if (data.event_type || data.event_id) {
              onEvent(data as CommerceEvent);
            }
          } catch {
            // Skip non-JSON messages (heartbeats, etc.)
          }
        };

        ws.onclose = () => {
          if (!closed) {
            setTimeout(connect, reconnectDelay);
            reconnectDelay = Math.min(reconnectDelay * 2, 30000);
          }
        };

        ws.onerror = (event) => {
          onError?.(new Error("WebSocket error"));
        };
      } catch (err) {
        onError?.(err instanceof Error ? err : new Error(String(err)));
        if (!closed) {
          setTimeout(connect, reconnectDelay);
          reconnectDelay = Math.min(reconnectDelay * 2, 30000);
        }
      }
    };

    connect();

    return () => {
      closed = true;
      ws?.close();
    };
  }
}
