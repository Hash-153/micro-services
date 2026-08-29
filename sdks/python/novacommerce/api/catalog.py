import httpx
from typing import Dict, Any, List

class CatalogApi:
    def __init__(self, client: httpx.AsyncClient):
        self._client = client

    async def list_products(self, page: int = 1, limit: int = 20) -> List[Dict[str, Any]]:
        resp = await self._client.get(f"/api/v1/catalog/products?page={page}&limit={limit}")
        resp.raise_for_status()
        return resp.json()["data"]

    async def get_product(self, product_id: str) -> Dict[str, Any]:
        resp = await self._client.get(f"/api/v1/catalog/products/{product_id}")
        resp.raise_for_status()
        return resp.json()["data"]
