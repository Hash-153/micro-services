import httpx
from typing import Dict, Any, List, Optional
from ..models.domain import Product, ProductVariant

class CatalogApi:
    def __init__(self, client: httpx.AsyncClient):
        self._client = client

    async def list_products(self, page: int = 1, limit: int = 20, query: Optional[str] = None, category_id: Optional[str] = None) -> List[Product]:
        params = {"page": page, "limit": limit}
        if query: params["query"] = query
        if category_id: params["categoryId"] = category_id
        resp = await self._client.get("/api/v1/catalog/products", params=params)
        resp.raise_for_status()
        items = resp.json().get("data", resp.json())
        return [Product(**p) for p in items]

    async def get_product(self, product_id: str) -> Product:
        resp = await self._client.get(f"/api/v1/catalog/products/{product_id}")
        resp.raise_for_status()
        return Product(**resp.json().get("data", resp.json()))

    async def create_product(self, product_data: Dict[str, Any]) -> Product:
        resp = await self._client.post("/api/v1/catalog/products", json=product_data)
        resp.raise_for_status()
        return Product(**resp.json().get("data", resp.json()))

    async def update_product(self, product_id: str, updates: Dict[str, Any]) -> Product:
        resp = await self._client.put(f"/api/v1/catalog/products/{product_id}", json=updates)
        resp.raise_for_status()
        return Product(**resp.json().get("data", resp.json()))

    async def delete_product(self, product_id: str) -> bool:
        resp = await self._client.delete(f"/api/v1/catalog/products/{product_id}")
        resp.raise_for_status()
        return True
