import httpx
from typing import Dict, Any, Optional

class AuthApi:
    def __init__(self, client: httpx.AsyncClient):
        self._client = client

    async def register(self, email: str, password: str, first_name: str, last_name: str, organization_name: Optional[str] = None) -> Dict[str, Any]:
        payload = {
            "email": email,
            "password": password,
            "firstName": first_name,
            "lastName": last_name,
            "organizationName": organization_name
        }
        resp = await self._client.post("/api/v1/auth/register", json=payload)
        resp.raise_for_status()
        return resp.json().get("data", resp.json())

    async def login(self, email: str, password: str, mfa_code: Optional[str] = None) -> Dict[str, Any]:
        payload = {"email": email, "password": password, "mfaCode": mfa_code}
        resp = await self._client.post("/api/v1/auth/login", json=payload)
        resp.raise_for_status()
        return resp.json().get("data", resp.json())

    async def refresh_token(self, refresh_token: str) -> Dict[str, Any]:
        payload = {"refreshToken": refresh_token}
        resp = await self._client.post("/api/v1/auth/refresh", json=payload)
        resp.raise_for_status()
        return resp.json().get("data", resp.json())

    async def get_current_user(self) -> Dict[str, Any]:
        resp = await self._client.get("/api/v1/auth/me")
        resp.raise_for_status()
        return resp.json().get("data", resp.json())

    async def setup_mfa(self) -> Dict[str, Any]:
        resp = await self._client.post("/api/v1/auth/mfa/setup")
        resp.raise_for_status()
        return resp.json().get("data", resp.json())

    async def verify_mfa(self, code: str) -> bool:
        resp = await self._client.post("/api/v1/auth/mfa/verify", json={"code": code})
        resp.raise_for_status()
        return True

    async def request_password_reset(self, email: str) -> bool:
        resp = await self._client.post("/api/v1/auth/password/reset-request", json={"email": email})
        resp.raise_for_status()
        return True
