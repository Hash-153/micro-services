import httpx
from typing import Dict, Any

class NotificationsApi:
    def __init__(self, client: httpx.AsyncClient):
        self._client = client

    async def send_notification(self, recipient: str, channel: str, template: str, data: Dict[str, Any]) -> Dict[str, Any]:
        payload = {
            "recipient": recipient,
            "channel": channel,
            "template": template,
            "data": data
        }
        resp = await self._client.post("/api/v1/notifications/send", json=payload)
        resp.raise_for_status()
        return resp.json().get("data", resp.json())

    async def list_templates(self) -> List[Dict[str, Any]]:
        resp = await self._client.get("/api/v1/notifications/templates")
        resp.raise_for_status()
        return resp.json().get("data", resp.json())
