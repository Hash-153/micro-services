import httpx
from typing import Dict, Any

class InventoryApi:
    def __init__(self, client: httpx.AsyncClient):
        self._client = client

    async def set_stock(self, sku: str, warehouse_id: str, quantity: int) -> Dict[str, Any]:
        resp = await self._client.post("/api/v1/inventory/stock", json={
            "sku": sku,
            "warehouseId": warehouse_id,
            "quantity": quantity
        })
        resp.raise_for_status()
        return resp.json()["data"]

    async def reserve_stock(self, order_id: str, sku: str, quantity: int) -> Dict[str, Any]:
        resp = await self._client.post("/api/v1/inventory/reserve", json={
            "orderId": order_id,
            "sku": sku,
            "quantity": quantity
        })
        resp.raise_for_status()
        return resp.json()["data"]
