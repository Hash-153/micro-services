import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created {path} ({len(content.splitlines())} lines)")

def build_python_sdk():
    print("Building comprehensive Python SDK...")
    pkg_dir = "sdks/python/novacommerce"

    # 1. Models
    write_file(f"{pkg_dir}/models/domain.py", """from enum import Enum
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime

class Currency(str, Enum):
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    CAD = "CAD"
    AUD = "AUD"
    JPY = "JPY"
    CHF = "CHF"
    SGD = "SGD"
    INR = "INR"

class OrderStatus(str, Enum):
    DRAFT = "DRAFT"
    PENDING_PAYMENT = "PENDING_PAYMENT"
    PAYMENT_AUTHORIZED = "PAYMENT_AUTHORIZED"
    PAYMENT_FAILED = "PAYMENT_FAILED"
    PROCESSING = "PROCESSING"
    INVENTORY_RESERVED = "INVENTORY_RESERVED"
    INVENTORY_ALLOCATION_FAILED = "INVENTORY_ALLOCATION_FAILED"
    PACKED = "PACKED"
    DISPATCHED = "DISPATCHED"
    IN_TRANSIT = "IN_TRANSIT"
    OUT_FOR_DELIVERY = "OUT_FOR_DELIVERY"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"
    REFUND_REQUESTED = "REFUND_REQUESTED"
    REFUNDED = "REFUNDED"
    PARTIALLY_REFUNDED = "PARTIALLY_REFUNDED"
    EXPIRED = "EXPIRED"

class PaymentStatus(str, Enum):
    PENDING = "PENDING"
    REQUIRES_ACTION = "REQUIRES_ACTION"
    PROCESSING = "PROCESSING"
    AUTHORIZED = "AUTHORIZED"
    CAPTURED = "CAPTURED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    REFUNDED = "REFUNDED"
    PARTIALLY_REFUNDED = "PARTIALLY_REFUNDED"
    DISPUTED = "DISPUTED"
    CHARGEBACK = "CHARGEBACK"

class UserRole(str, Enum):
    SUPER_ADMIN = "SUPER_ADMIN"
    ADMIN = "ADMIN"
    OPERATIONS_MANAGER = "OPERATIONS_MANAGER"
    INVENTORY_MANAGER = "INVENTORY_MANAGER"
    FINANCE_ANALYST = "FINANCE_ANALYST"
    SUPPORT_AGENT = "SUPPORT_AGENT"
    CUSTOMER = "CUSTOMER"
    GUEST = "GUEST"
    SYSTEM_INTERNAL = "SYSTEM_INTERNAL"

class Money(BaseModel):
    amount: int = Field(..., description="Monetary value stored in minor currency units (cents)")
    currency: Currency = Currency.USD

class Address(BaseModel):
    id: Optional[str] = None
    recipient_name: str
    company_name: Optional[str] = None
    street_line1: str
    street_line2: Optional[str] = None
    city: str
    state_or_province: str
    postal_code: str
    country_code: str
    is_default_shipping: bool = False
    is_default_billing: bool = False
    phone: Optional[str] = None

class ProductVariant(BaseModel):
    id: str
    product_id: str
    sku: str
    name: str
    price_modifier_cents: int = 0
    weight_grams: int = 500
    length_mm: int = 100
    width_mm: int = 100
    height_mm: int = 100
    options: Dict[str, str] = Field(default_factory=dict)
    is_active: bool = True

class Product(BaseModel):
    id: str
    sku: str
    name: str
    slug: str
    description: str
    category_id: str
    base_price: Money
    is_active: bool = True
    is_featured: bool = False
    tags: List[str] = Field(default_factory=list)
    attributes: Dict[str, Any] = Field(default_factory=dict)
    variants: List[ProductVariant] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime

class OrderItem(BaseModel):
    id: str
    order_id: str
    sku: str
    product_name: str
    variant_name: Optional[str] = None
    unit_price: Money
    quantity: int
    subtotal: Money
    tax_amount: Money
    discount_amount: Money
    total: Money

class Order(BaseModel):
    id: str
    order_number: str
    user_id: str
    status: OrderStatus
    items: List[OrderItem]
    subtotal_amount: Money
    tax_amount: Money
    shipping_fee_amount: Money
    discount_amount: Money
    total_amount: Money
    shipping_address: Address
    billing_address: Address
    coupon_code: Optional[str] = None
    payment_id: Optional[str] = None
    shipment_id: Optional[str] = None
    idempotency_key: str
    created_at: datetime
    updated_at: datetime

class PaymentTransaction(BaseModel):
    id: str
    transaction_reference: str
    order_id: str
    user_id: str
    amount: Money
    status: PaymentStatus
    method_type: str
    provider: str
    provider_transaction_id: Optional[str] = None
    failure_reason: Optional[str] = None
    idempotency_key: str
    created_at: datetime

class InventoryStock(BaseModel):
    id: str
    sku: str
    warehouse_id: str
    on_hand_quantity: int
    reserved_quantity: int
    allocated_quantity: int
    safety_stock_threshold: int
    reorder_quantity: int
    bin_location: Optional[str] = None
    version: int

class Shipment(BaseModel):
    id: str
    shipment_number: str
    order_id: str
    status: str
    carrier: str
    service_level: str
    tracking_number: Optional[str] = None
    tracking_url: Optional[str] = None
    shipping_label_url: Optional[str] = None
    origin_warehouse_id: str
    destination_address: Address
    weight_grams: int
    created_at: datetime
""")

    # 2. Exceptions
    write_file(f"{pkg_dir}/exceptions.py", """class NovaCommerceException(Exception):
    def __init__(self, message: str, status_code: int = 500, error_code: str = "ERR_INTERNAL_ERROR", details: Any = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.details = details

class AuthenticationError(NovaCommerceException):
    def __init__(self, message: str = "Invalid credentials or expired token"):
        super().__init__(message, status_code=401, error_code="ERR_AUTH_UNAUTHORIZED")

class PermissionDeniedError(NovaCommerceException):
    def __init__(self, message: str = "Insufficient permissions for requested action"):
        super().__init__(message, status_code=403, error_code="ERR_FORBIDDEN")

class NotFoundError(NovaCommerceException):
    def __init__(self, resource: str, resource_id: str):
        super().__init__(f"{resource} '{resource_id}' was not found", status_code=404, error_code="ERR_NOT_FOUND")

class ValidationError(NovaCommerceException):
    def __init__(self, message: str, details: Any = None):
        super().__init__(message, status_code=400, error_code="ERR_VALIDATION_FAILED", details=details)

class InsufficientStockError(NovaCommerceException):
    def __init__(self, sku: str, requested: int, available: int):
        super().__init__(f"Insufficient stock for SKU {sku}: requested {requested}, available {available}", status_code=409, error_code="ERR_INSUFFICIENT_STOCK")

class SagaExecutionError(NovaCommerceException):
    def __init__(self, saga_name: str, step_name: str, reason: str):
        super().__init__(f"Saga '{saga_name}' failed at step '{step_name}': {reason}", status_code=500, error_code="ERR_SAGA_FAILED")
""")

    # 3. Client & APIs
    write_file(f"{pkg_dir}/client.py", """import httpx
from typing import Optional, Dict, Any, List
from .models.domain import Product, Order, PaymentTransaction, InventoryStock, Shipment, Address, Money, Currency
from .exceptions import NovaCommerceException, AuthenticationError, NotFoundError, ValidationError

class NovaCommerceClient:
    def __init__(
        self,
        base_url: str = "http://localhost:8000",
        api_key: Optional[str] = None,
        auth_token: Optional[str] = None,
        timeout: float = 30.0,
        max_retries: int = 3
    ):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.auth_token = auth_token
        self.timeout = timeout
        self.max_retries = max_retries
        self._http_client = httpx.AsyncClient(base_url=self.base_url, timeout=self.timeout)

    def set_auth_token(self, token: str) -> None:
        self.auth_token = token

    def _get_headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        if self.auth_token:
            headers["Authorization"] = f"Bearer {self.auth_token}"
        elif self.api_key:
            headers["X-API-Key"] = self.api_key
        return headers

    async def _request(self, method: str, path: str, json: Optional[Dict[str, Any]] = None, params: Optional[Dict[str, Any]] = None) -> Any:
        headers = self._get_headers()
        resp = await self._http_client.request(method, path, json=json, params=params, headers=headers)
        if resp.status_code >= 400:
            self._handle_error(resp)
        data = resp.json()
        return data.get("data", data)

    def _handle_error(self, resp: httpx.Response) -> None:
        try:
            body = resp.json()
            err_info = body.get("error", {})
            msg = err_info.get("message", resp.text)
            code = err_info.get("code", "ERR_API_ERROR")
            details = err_info.get("details")
        except Exception:
            msg = resp.text
            code = "ERR_HTTP_ERROR"
            details = None

        if resp.status_code == 401:
            raise AuthenticationError(msg)
        elif resp.status_code == 404:
            raise NotFoundError("Resource", path := resp.url.path)
        elif resp.status_code == 400:
            raise ValidationError(msg, details)
        else:
            raise NovaCommerceException(msg, status_code=resp.status_code, error_code=code, details=details)

    # Catalog Methods
    async def list_products(self, page: int = 1, limit: int = 20, category_id: Optional[str] = None) -> List[Product]:
        params = {"page": page, "limit": limit}
        if category_id:
            params["categoryId"] = category_id
        res = await self._request("GET", "/api/v1/catalog/products", params=params)
        return [Product(**item) for item in res]

    async def get_product_by_id(self, product_id: str) -> Product:
        res = await self._request("GET", f"/api/v1/catalog/products/{product_id}")
        return Product(**res)

    async def get_product_by_sku(self, sku: str) -> Product:
        res = await self._request("GET", f"/api/v1/catalog/products/sku/{sku}")
        return Product(**res)

    # Order Methods
    async def create_order(self, user_id: str, items: List[Dict[str, Any]], shipping_address: Dict[str, Any], billing_address: Dict[str, Any], coupon_code: Optional[str] = None) -> Order:
        payload = {
            "userId": user_id,
            "items": items,
            "shippingAddress": shipping_address,
            "billingAddress": billing_address,
            "couponCode": coupon_code
        }
        res = await self._request("POST", "/api/v1/orders", json=payload)
        return Order(**res)

    async def get_order_by_id(self, order_id: str) -> Order:
        res = await self._request("GET", f"/api/v1/orders/{order_id}")
        return Order(**res)

    async def execute_checkout_saga(self, order_id: str) -> Dict[str, Any]:
        return await self._request("POST", f"/api/v1/orders/{order_id}/checkout-saga")

    # Payment Methods
    async def authorize_payment(self, order_id: str, amount_cents: int, currency: Currency = Currency.USD) -> PaymentTransaction:
        payload = {"orderId": order_id, "amountCents": amount_cents, "currency": currency.value}
        res = await self._request("POST", "/api/v1/payments/authorize", json=payload)
        return PaymentTransaction(**res)

    # Inventory Methods
    async def get_stock(self, sku: str) -> InventoryStock:
        res = await self._request("GET", f"/api/v1/inventory/stock/{sku}")
        return InventoryStock(**res)

    async def reserve_stock(self, order_id: str, sku: str, quantity: int) -> Dict[str, Any]:
        payload = {"orderId": order_id, "sku": sku, "quantity": quantity}
        return await self._request("POST", "/api/v1/inventory/reserve", json=payload)

    # Fulfillment Methods
    async def create_shipment(self, order_id: str, destination_address: Dict[str, Any], carrier: str = "FEDEX") -> Shipment:
        payload = {"orderId": order_id, "destinationAddress": destination_address, "carrier": carrier}
        res = await self._request("POST", "/api/v1/fulfillment/shipments", json=payload)
        return Shipment(**res)

    async def close(self) -> None:
        await self._http_client.aclose()
""")

    print("Python SDK generated.")

if __name__ == "__main__":
    build_python_sdk()
