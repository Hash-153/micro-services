import httpx
from typing import Dict, Any

class AuthApi:
    def __init__(self, client: httpx.AsyncClient):
        self._client = client

    async def register(self, email: str, password: str, first_name: str, last_name: str) -> Dict[str, Any]:
        resp = await self._client.post("/api/v1/auth/register", json={
            "email": email,
            "password": password,
            "firstName": first_name,
            "lastName": last_name
        })
        resp.raise_for_status()
        return resp.json()["data"]

    async def login(self, email: str, password: str) -> Dict[str, Any]:
        resp = await self._client.post("/api/v1/auth/login", json={
            "email": email,
            "password": password
        })
        resp.raise_for_status()
        return resp.json()["data"]
