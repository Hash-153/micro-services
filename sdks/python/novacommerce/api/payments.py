import httpx
from typing import Dict, Any

class PaymentsApi:
    def __init__(self, client: httpx.AsyncClient):
        self._client = client

    async def authorize(self, order_id: str, amount_cents: int, currency: str = "USD") -> Dict[str, Any]:
        resp = await self._client.post("/api/v1/payments/authorize", json={
            "orderId": order_id,
            "amountCents": amount_cents,
            "currency": currency
        })
        resp.raise_for_status()
        return resp.json()["data"]
