import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def generate_sdk_python_expansion():
    print("Expanding Python SDK with exhaustive API modules...")
    pkg = "sdks/python/novacommerce/api"

    write_file(f"{pkg}/auth.py", """import httpx
from typing import Dict, Any, Optional

class AuthApi:
    def __init__(self, client: httpx.AsyncClient):
        self._client = client

    async def register(self, email: str, password: str, first_name: str, last_name: str, organization_name: Optional[str] = None) -> Dict[str, Any]:
        payload = {
            "email": email,
            "password": password,
            "firstName": first_name,
            "lastName": last_name,
            "organizationName": organization_name
        }
        resp = await self._client.post("/api/v1/auth/register", json=payload)
        resp.raise_for_status()
        return resp.json().get("data", resp.json())

    async def login(self, email: str, password: str, mfa_code: Optional[str] = None) -> Dict[str, Any]:
        payload = {"email": email, "password": password, "mfaCode": mfa_code}
        resp = await self._client.post("/api/v1/auth/login", json=payload)
        resp.raise_for_status()
        return resp.json().get("data", resp.json())

    async def refresh_token(self, refresh_token: str) -> Dict[str, Any]:
        payload = {"refreshToken": refresh_token}
        resp = await self._client.post("/api/v1/auth/refresh", json=payload)
        resp.raise_for_status()
        return resp.json().get("data", resp.json())

    async def get_current_user(self) -> Dict[str, Any]:
        resp = await self._client.get("/api/v1/auth/me")
        resp.raise_for_status()
        return resp.json().get("data", resp.json())

    async def setup_mfa(self) -> Dict[str, Any]:
        resp = await self._client.post("/api/v1/auth/mfa/setup")
        resp.raise_for_status()
        return resp.json().get("data", resp.json())

    async def verify_mfa(self, code: str) -> bool:
        resp = await self._client.post("/api/v1/auth/mfa/verify", json={"code": code})
        resp.raise_for_status()
        return True

    async def request_password_reset(self, email: str) -> bool:
        resp = await self._client.post("/api/v1/auth/password/reset-request", json={"email": email})
        resp.raise_for_status()
        return True
""")

    write_file(f"{pkg}/catalog.py", """import httpx
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
""")

    write_file(f"{pkg}/inventory.py", """import httpx
from typing import Dict, Any, List, Optional
from ..models.domain import InventoryStock

class InventoryApi:
    def __init__(self, client: httpx.AsyncClient):
        self._client = client

    async def get_stock(self, sku: str) -> InventoryStock:
        resp = await self._client.get(f"/api/v1/inventory/stock/{sku}")
        resp.raise_for_status()
        return InventoryStock(**resp.json().get("data", resp.json()))

    async def adjust_stock(self, sku: str, warehouse_id: str, quantity: int) -> InventoryStock:
        payload = {"sku": sku, "warehouseId": warehouse_id, "quantity": quantity}
        resp = await self._client.post("/api/v1/inventory/stock", json=payload)
        resp.raise_for_status()
        return InventoryStock(**resp.json().get("data", resp.json()))

    async def reserve_stock(self, order_id: str, sku: str, quantity: int) -> Dict[str, Any]:
        payload = {"orderId": order_id, "sku": sku, "quantity": quantity}
        resp = await self._client.post("/api/v1/inventory/reserve", json=payload)
        resp.raise_for_status()
        return resp.json().get("data", resp.json())

    async def release_stock(self, order_id: str) -> bool:
        resp = await self._client.post("/api/v1/inventory/release", json={"orderId": order_id})
        resp.raise_for_status()
        return True

    async def get_reorder_advice(self, sku: str) -> Dict[str, Any]:
        resp = await self._client.get(f"/api/v1/inventory/reorder-advice", params={"sku": sku})
        resp.raise_for_status()
        return resp.json().get("data", resp.json())
""")

    write_file(f"{pkg}/orders.py", """import httpx
from typing import Dict, Any, List, Optional
from ..models.domain import Order

class OrdersApi:
    def __init__(self, client: httpx.AsyncClient):
        self._client = client

    async def create_order(self, order_payload: Dict[str, Any]) -> Order:
        resp = await self._client.post("/api/v1/orders", json=order_payload)
        resp.raise_for_status()
        return Order(**resp.json().get("data", resp.json()))

    async def get_order(self, order_id: str) -> Order:
        resp = await self._client.get(f"/api/v1/orders/{order_id}")
        resp.raise_for_status()
        return Order(**resp.json().get("data", resp.json()))

    async def list_orders(self, page: int = 1, limit: int = 20, user_id: Optional[str] = None) -> List[Order]:
        params = {"page": page, "limit": limit}
        if user_id: params["userId"] = user_id
        resp = await self._client.get("/api/v1/orders", params=params)
        resp.raise_for_status()
        items = resp.json().get("data", resp.json())
        return [Order(**o) for o in items]

    async def cancel_order(self, order_id: str, reason: str = "Customer request") -> Order:
        resp = await self._client.post(f"/api/v1/orders/{order_id}/cancel", json={"reason": reason})
        resp.raise_for_status()
        return Order(**resp.json().get("data", resp.json()))

    async def execute_checkout_saga(self, order_id: str) -> Dict[str, Any]:
        resp = await self._client.post(f"/api/v1/orders/{order_id}/checkout-saga")
        resp.raise_for_status()
        return resp.json().get("data", resp.json())

    async def get_invoice_html(self, order_id: str) -> str:
        resp = await self._client.get(f"/api/v1/orders/{order_id}/invoice")
        resp.raise_for_status()
        return resp.text
""")

    write_file(f"{pkg}/payments.py", """import httpx
from typing import Dict, Any, Optional
from ..models.domain import PaymentTransaction, Currency

class PaymentsApi:
    def __init__(self, client: httpx.AsyncClient):
        self._client = client

    async def authorize_payment(self, order_id: str, amount_cents: int, currency: Currency = Currency.USD, method_type: str = "CREDIT_CARD", token: str = "tok_visa") -> PaymentTransaction:
        payload = {
            "orderId": order_id,
            "amountCents": amount_cents,
            "currency": currency.value,
            "methodType": method_type,
            "paymentMethodToken": token
        }
        resp = await self._client.post("/api/v1/payments/authorize", json=payload)
        resp.raise_for_status()
        return PaymentTransaction(**resp.json().get("data", resp.json()))

    async def capture_payment(self, transaction_id: str) -> PaymentTransaction:
        resp = await self._client.post(f"/api/v1/payments/{transaction_id}/capture")
        resp.raise_for_status()
        return PaymentTransaction(**resp.json().get("data", resp.json()))

    async def refund_payment(self, transaction_id: str, amount_cents: Optional[int] = None, reason: str = "Customer refund") -> PaymentTransaction:
        payload = {"amountCents": amount_cents, "reason": reason}
        resp = await self._client.post(f"/api/v1/payments/{transaction_id}/refund", json=payload)
        resp.raise_for_status()
        return PaymentTransaction(**resp.json().get("data", resp.json()))

    async def get_trial_balance(self) -> Dict[str, Any]:
        resp = await self._client.get("/api/v1/payments/ledger/reconcile")
        resp.raise_for_status()
        return resp.json().get("data", resp.json())
""")

    write_file(f"{pkg}/fulfillment.py", """import httpx
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
""")

    print("Python SDK expansion generated.")

if __name__ == "__main__":
    generate_sdk_python_expansion()
