import httpx
from typing import Dict, Any

class FulfillmentApi:
    def __init__(self, client: httpx.AsyncClient):
        self._client = client

    async def create_shipment(self, order_id: str, destination_address: Dict[str, Any], carrier: str = "FEDEX") -> Dict[str, Any]:
        resp = await self._client.post("/api/v1/fulfillment/shipments", json={
            "orderId": order_id,
            "destinationAddress": destination_address,
            "carrier": carrier
        })
        resp.raise_for_status()
        return resp.json()["data"]
