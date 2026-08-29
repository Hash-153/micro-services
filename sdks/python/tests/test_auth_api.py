import pytest
import httpx
from novacommerce.api.auth import AuthApi

@pytest.mark.asyncio
async def test_auth_api_init():
    client = httpx.AsyncClient()
    auth_api = AuthApi(client)
    assert auth_api is not None
    await client.aclose()
