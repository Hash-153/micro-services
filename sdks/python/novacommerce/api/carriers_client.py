import httpx
from typing import Dict, Any, List, Optional
from pydantic import BaseModel

class CarrierClientFilterOptions(BaseModel):
    page: int = 1
    limit: int = 20
    search: Optional[str] = None
    sort_by: Optional[str] = None
    sort_order: Optional[str] = "desc"

class CarrierClient:
    """Logistics carrier accounts and customs documentation"""
    def __init__(self, http_client: httpx.AsyncClient, base_url: str):
        self.http_client = http_client
        self.base_url = base_url.rstrip('/') + "/api/v1/carriers"

    async def get_by_id(self, item_id: str) -> Dict[str, Any]:
        resp = await self.http_client.get(f"{self.base_url}/{item_id}")
        resp.raise_for_status()
        return resp.json().get("data", {})

    async def list(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        resp = await self.http_client.get(self.base_url, params=params or {})
        resp.raise_for_status()
        return resp.json().get("data", {})

    async def create(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        resp = await self.http_client.post(self.base_url, json=payload)
        resp.raise_for_status()
        return resp.json().get("data", {})

    async def update(self, item_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        resp = await self.http_client.put(f"{self.base_url}/{item_id}", json=payload)
        resp.raise_for_status()
        return resp.json().get("data", {})

    async def patch(self, item_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        resp = await self.http_client.patch(f"{self.base_url}/{item_id}", json=payload)
        resp.raise_for_status()
        return resp.json().get("data", {})

    async def delete(self, item_id: str) -> bool:
        resp = await self.http_client.delete(f"{self.base_url}/{item_id}")
        resp.raise_for_status()
        return bool(resp.json().get("data", True))
