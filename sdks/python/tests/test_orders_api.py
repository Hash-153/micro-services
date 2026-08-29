import pytest
import httpx
from novacommerce.api.orders import OrdersApi

@pytest.mark.asyncio
async def test_orders_api_init():
    client = httpx.AsyncClient()
    orders_api = OrdersApi(client)
    assert orders_api is not None
    await client.aclose()
