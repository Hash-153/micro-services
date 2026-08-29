import httpx
from typing import Optional, List, Dict, Any
from .models import User, Product, Order, Money

class NovaCommerceClient:
    def __init__(self, base_url: str = "http://localhost:8000", access_token: Optional[str] = None):
        self.base_url = base_url.rstrip("/")
        self.access_token = access_token
        self._client = httpx.AsyncClient(base_url=self.base_url, timeout=30.0)

    def set_token(self, token: str) -> None:
        self.access_token = token

    async def close(self) -> None:
        await self._client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
