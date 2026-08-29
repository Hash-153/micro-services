# NovaCommerce Python Client SDK

Official Python Async SDK for NovaCommerce Microservices Distributed Platform.

```python
import asyncio
from novacommerce import NovaCommerceClient

async def main():
    client = NovaCommerceClient(base_url="http://localhost:8000")
    auth_resp = await client.auth.login("admin@novacommerce.io", "AdminSecure123!")
    print("Logged in successfully:", auth_resp.user_id)

asyncio.run(main())
```
