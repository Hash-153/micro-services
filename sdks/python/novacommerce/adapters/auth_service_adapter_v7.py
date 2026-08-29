import httpx
from typing import Dict, Any, List, Optional
from pydantic import BaseModel

class AuthServiceAsyncAdapterV7Config(BaseModel):
    service_name: str = "auth-service"
    version: int = 7
    timeout_seconds: float = 15.0
    retry_max_attempts: int = 3
    backoff_multiplier: float = 1.5

class AuthServiceAsyncAdapterV7:
    """High-performance async adapter for auth-service version 7"""
    def __init__(self, client: httpx.AsyncClient, base_url: str, config: Optional[AuthServiceAsyncAdapterV7Config] = None):
        self.client = client
        self.base_url = base_url.rstrip('/') + "/api/v7/auth"
        self.config = config or AuthServiceAsyncAdapterV7Config()

    async def execute_query(self, endpoint_suffix: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = f"{self.base_url}/{endpoint_suffix.lstrip('/')}"
        resp = await self.client.get(url, params=params or {}, timeout=self.config.timeout_seconds)
        resp.raise_for_status()
        return resp.json()

    async def execute_mutation(self, endpoint_suffix: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}/{endpoint_suffix.lstrip('/')}"
        resp = await self.client.post(url, json=payload, timeout=self.config.timeout_seconds)
        resp.raise_for_status()
        return resp.json()

    async def check_health(self) -> Dict[str, Any]:
        url = f"{self.base_url}/health/diagnostics"
        resp = await self.client.get(url, timeout=5.0)
        return resp.json()
