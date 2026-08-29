import httpx
from typing import Dict, Any, Optional

class AnalyticsApi:
    def __init__(self, client: httpx.AsyncClient):
        self._client = client

    async def track_event(self, event_name: str, properties: Dict[str, Any], user_id: Optional[str] = None) -> bool:
        payload = {"eventName": event_name, "properties": properties}
        if user_id: payload["userId"] = user_id
        resp = await self._client.post("/api/v1/analytics/events", json=payload)
        resp.raise_for_status()
        return True

    async def get_summary(self) -> Dict[str, Any]:
        resp = await self._client.get("/api/v1/analytics/summary")
        resp.raise_for_status()
        return resp.json().get("data", resp.json())

    async def get_revenue_rollup(self) -> Dict[str, Any]:
        resp = await self._client.get("/api/v1/analytics/revenue-rollup")
        resp.raise_for_status()
        return resp.json().get("data", resp.json())
