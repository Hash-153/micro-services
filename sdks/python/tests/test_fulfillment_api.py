import pytest
import httpx
from novacommerce.api.fulfillment import FulfillmentApi

@pytest.mark.asyncio
async def test_fulfillment_api_init():
    client = httpx.AsyncClient()
    fulfillment_api = FulfillmentApi(client)
    assert fulfillment_api is not None
    await client.aclose()
