import pytest
import httpx
from novacommerce.api.inventory import InventoryApi

@pytest.mark.asyncio
async def test_inventory_api_init():
    client = httpx.AsyncClient()
    inventory_api = InventoryApi(client)
    assert inventory_api is not None
    await client.aclose()
