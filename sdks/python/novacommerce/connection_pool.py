import asyncio
import httpx
from typing import Optional, Dict, Any

class AsyncConnectionPoolManager:
    def __init__(self, max_connections: int = 100, max_keepalive_connections: int = 20, keepalive_expiry: float = 30.0):
        self.limits = httpx.Limits(
            max_connections=max_connections,
            max_keepalive_connections=max_keepalive_connections,
            keepalive_expiry=keepalive_expiry
        )
        self.timeout = httpx.Timeout(30.0, connect=5.0, read=25.0, write=5.0)

    def create_client(self, base_url: str, default_headers: Optional[Dict[str, str]] = None) -> httpx.AsyncClient:
        return httpx.AsyncClient(
            base_url=base_url,
            headers=default_headers or {},
            limits=self.limits,
            timeout=self.timeout,
            http2=True
        )
