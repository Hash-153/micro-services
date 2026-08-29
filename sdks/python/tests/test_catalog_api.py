import pytest
import httpx
from novacommerce.api.catalog import CatalogApi

@pytest.mark.asyncio
async def test_catalog_api_init():
    client = httpx.AsyncClient()
    catalog_api = CatalogApi(client)
    assert catalog_api is not None
    await client.aclose()
