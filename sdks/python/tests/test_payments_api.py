import pytest
import httpx
from novacommerce.api.payments import PaymentsApi

@pytest.mark.asyncio
async def test_payments_api_init():
    client = httpx.AsyncClient()
    payments_api = PaymentsApi(client)
    assert payments_api is not None
    await client.aclose()
