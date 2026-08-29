import httpx
from typing import Dict, Any

class OrdersApi:
    def __init__(self, client: httpx.AsyncClient):
        self._client = client

    async def create_order(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        resp = await self._client.post("/api/v1/orders", json=order_data)
        resp.raise_for_status()
        return resp.json()["data"]

    async def get_order(self, order_id: str) -> Dict[str, Any]:
        resp = await self._client.get(f"/api/v1/orders/{order_id}")
        resp.raise_for_status()
        return resp.json()["data"]
