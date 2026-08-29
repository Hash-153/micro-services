import httpx
from typing import Dict, Any, List, Optional
from pydantic import BaseModel

class CatalogServiceAsyncAdapterV9Config(BaseModel):
    service_name: str = "catalog-service"
    version: int = 9
    timeout_seconds: float = 15.0
    retry_max_attempts: int = 3
    backoff_multiplier: float = 1.5

class CatalogServiceAsyncAdapterV9:
    """High-performance async adapter for catalog-service version 9"""
    def __init__(self, client: httpx.AsyncClient, base_url: str, config: Optional[CatalogServiceAsyncAdapterV9Config] = None):
        self.client = client
        self.base_url = base_url.rstrip('/') + "/api/v9/catalog"
        self.config = config or CatalogServiceAsyncAdapterV9Config()

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
