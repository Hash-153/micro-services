import httpx
from typing import Dict, Any, List, Optional
from ..models.domain import Order

class OrdersApi:
    def __init__(self, client: httpx.AsyncClient):
        self._client = client

    async def create_order(self, order_payload: Dict[str, Any]) -> Order:
        resp = await self._client.post("/api/v1/orders", json=order_payload)
        resp.raise_for_status()
        return Order(**resp.json().get("data", resp.json()))

    async def get_order(self, order_id: str) -> Order:
        resp = await self._client.get(f"/api/v1/orders/{order_id}")
        resp.raise_for_status()
        return Order(**resp.json().get("data", resp.json()))

    async def list_orders(self, page: int = 1, limit: int = 20, user_id: Optional[str] = None) -> List[Order]:
        params = {"page": page, "limit": limit}
        if user_id: params["userId"] = user_id
        resp = await self._client.get("/api/v1/orders", params=params)
        resp.raise_for_status()
        items = resp.json().get("data", resp.json())
        return [Order(**o) for o in items]

    async def cancel_order(self, order_id: str, reason: str = "Customer request") -> Order:
        resp = await self._client.post(f"/api/v1/orders/{order_id}/cancel", json={"reason": reason})
        resp.raise_for_status()
        return Order(**resp.json().get("data", resp.json()))

    async def execute_checkout_saga(self, order_id: str) -> Dict[str, Any]:
        resp = await self._client.post(f"/api/v1/orders/{order_id}/checkout-saga")
        resp.raise_for_status()
        return resp.json().get("data", resp.json())

    async def get_invoice_html(self, order_id: str) -> str:
        resp = await self._client.get(f"/api/v1/orders/{order_id}/invoice")
        resp.raise_for_status()
        return resp.text
