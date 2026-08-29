import httpx
from typing import Dict, Any, List, Optional

class UserApi:
    def __init__(self, client: httpx.AsyncClient):
        self._client = client

    async def get_profile(self) -> Dict[str, Any]:
        resp = await self._client.get("/api/v1/users/profile")
        resp.raise_for_status()
        return resp.json().get("data", resp.json())

    async def update_profile(self, first_name: Optional[str] = None, last_name: Optional[str] = None, timezone: Optional[str] = None) -> Dict[str, Any]:
        payload = {}
        if first_name: payload["firstName"] = first_name
        if last_name: payload["lastName"] = last_name
        if timezone: payload["timezone"] = timezone
        resp = await self._client.put("/api/v1/users/profile", json=payload)
        resp.raise_for_status()
        return resp.json().get("data", resp.json())

    async def list_addresses(self) -> List[Dict[str, Any]]:
        resp = await self._client.get("/api/v1/users/addresses")
        resp.raise_for_status()
        return resp.json().get("data", resp.json())

    async def add_address(self, address_data: Dict[str, Any]) -> Dict[str, Any]:
        resp = await self._client.post("/api/v1/users/addresses", json=address_data)
        resp.raise_for_status()
        return resp.json().get("data", resp.json())

    async def delete_address(self, address_id: str) -> bool:
        resp = await self._client.delete(f"/api/v1/users/addresses/{address_id}")
        resp.raise_for_status()
        return True
