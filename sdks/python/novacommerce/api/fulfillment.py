import httpx
from typing import Dict, Any, List
from ..models.domain import Shipment

class FulfillmentApi:
    def __init__(self, client: httpx.AsyncClient):
        self._client = client

    async def create_shipment(self, order_id: str, destination_address: Dict[str, Any], carrier: str = "FEDEX", service_level: str = "GROUND") -> Shipment:
        payload = {
            "orderId": order_id,
            "destinationAddress": destination_address,
            "carrier": carrier,
            "serviceLevel": service_level
        }
        resp = await self._client.post("/api/v1/fulfillment/shipments", json=payload)
        resp.raise_for_status()
        return Shipment(**resp.json().get("data", resp.json()))

    async def get_shipment(self, shipment_id: str) -> Shipment:
        resp = await self._client.get(f"/api/v1/fulfillment/shipments/{shipment_id}")
        resp.raise_for_status()
        return Shipment(**resp.json().get("data", resp.json()))

    async def calculate_rates(self, request_payload: Dict[str, Any]) -> List[Dict[str, Any]]:
        resp = await self._client.post("/api/v1/fulfillment/rates", json=request_payload)
        resp.raise_for_status()
        return resp.json().get("data", resp.json())
