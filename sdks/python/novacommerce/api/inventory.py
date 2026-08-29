import httpx
from typing import Dict, Any, List, Optional
from ..models.domain import InventoryStock

class InventoryApi:
    def __init__(self, client: httpx.AsyncClient):
        self._client = client

    async def get_stock(self, sku: str) -> InventoryStock:
        resp = await self._client.get(f"/api/v1/inventory/stock/{sku}")
        resp.raise_for_status()
        return InventoryStock(**resp.json().get("data", resp.json()))

    async def adjust_stock(self, sku: str, warehouse_id: str, quantity: int) -> InventoryStock:
        payload = {"sku": sku, "warehouseId": warehouse_id, "quantity": quantity}
        resp = await self._client.post("/api/v1/inventory/stock", json=payload)
        resp.raise_for_status()
        return InventoryStock(**resp.json().get("data", resp.json()))

    async def reserve_stock(self, order_id: str, sku: str, quantity: int) -> Dict[str, Any]:
        payload = {"orderId": order_id, "sku": sku, "quantity": quantity}
        resp = await self._client.post("/api/v1/inventory/reserve", json=payload)
        resp.raise_for_status()
        return resp.json().get("data", resp.json())

    async def release_stock(self, order_id: str) -> bool:
        resp = await self._client.post("/api/v1/inventory/release", json={"orderId": order_id})
        resp.raise_for_status()
        return True

    async def get_reorder_advice(self, sku: str) -> Dict[str, Any]:
        resp = await self._client.get(f"/api/v1/inventory/reorder-advice", params={"sku": sku})
        resp.raise_for_status()
        return resp.json().get("data", resp.json())
