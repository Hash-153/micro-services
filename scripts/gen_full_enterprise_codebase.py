import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def build_full_enterprise_codebase():
    print("Building full enterprise codebase...")

    # -------------------------------------------------------------------------
    # 1. CORE TYPES: DTOs & Validation Schemas
    # -------------------------------------------------------------------------
    write_file("packages/core-types/src/dtos.ts", """import { UserRole, OrderStatus, PaymentStatus, FulfillmentStatus, Currency, KycStatus, AccountStatus } from './enums.js';
import { Money, AddressEntity, Dimensions3D } from './domain-models.js';

export interface RegisterUserDTO {
  email: string;
  password: string;
  firstName: string;
  lastName: string;
  role?: UserRole;
  organizationName?: string;
  phoneNumber?: string;
}

export interface LoginUserDTO {
  email: string;
  password: string;
  mfaCode?: string;
  deviceFingerprint?: string;
}

export interface AuthTokensResponseDTO {
  accessToken: string;
  refreshToken: string;
  tokenType: 'Bearer';
  expiresIn: number;
  user: {
    id: string;
    email: string;
    role: UserRole;
    status: AccountStatus;
    organizationId?: string | null;
  };
}

export interface RefreshTokenDTO {
  refreshToken: string;
}

export interface CreateProductDTO {
  sku: string;
  name: string;
  description: string;
  categoryId: string;
  basePrice: Money;
  tags?: string[];
  attributes?: Record<string, any>;
  images?: { url: string; altText?: string; isPrimary: boolean; sortOrder: number }[];
}

export interface UpdateProductDTO {
  name?: string;
  description?: string;
  categoryId?: string;
  basePrice?: Money;
  isActive?: boolean;
  isFeatured?: boolean;
  tags?: string[];
  attributes?: Record<string, any>;
}

export interface CreateOrderDTO {
  userId: string;
  items: {
    sku: string;
    productName: string;
    variantName?: string;
    quantity: number;
    unitPrice: Money;
  }[];
  shippingAddress: AddressEntity;
  billingAddress: AddressEntity;
  couponCode?: string;
  idempotencyKey: string;
}

export interface AuthorizePaymentDTO {
  orderId: string;
  userId: string;
  amount: Money;
  methodType: 'CREDIT_CARD' | 'DEBIT_CARD' | 'BANK_TRANSFER' | 'PAYPAL' | 'APPLE_PAY';
  paymentMethodToken: string;
  idempotencyKey: string;
}

export interface CreateShipmentDTO {
  orderId: string;
  destinationAddress: AddressEntity;
  carrier: 'FEDEX' | 'UPS' | 'DHL' | 'USPS';
  serviceLevel: string;
  weightGrams: number;
  dimensionsMm: Dimensions3D;
}
""")

    # -------------------------------------------------------------------------
    # 2. PYTHON SDK API CLIENTS
    # -------------------------------------------------------------------------
    pkg_py = "sdks/python/novacommerce/api"
    
    write_file(f"{pkg_py}/user.py", """import httpx
from typing import Dict, Any, List, Optional

class UserApi:
    def __init__(self, client: httpx.AsyncClient):
        self._client = client

    async def get_profile(self) -> Dict[str, Any]:
        resp = await self._client.get("/api/v1/users/profile")
        resp.raise_for_status()
        return resp.json().get("data", resp.json())

    async def update_profile(self, first_name: Optional[str] = None, last_name: Optional[str] = None, timezone: Optional[str] = None) -> Dict[str, Any]:
        payload = {}
        if first_name: payload["firstName"] = first_name
        if last_name: payload["lastName"] = last_name
        if timezone: payload["timezone"] = timezone
        resp = await self._client.put("/api/v1/users/profile", json=payload)
        resp.raise_for_status()
        return resp.json().get("data", resp.json())

    async def list_addresses(self) -> List[Dict[str, Any]]:
        resp = await self._client.get("/api/v1/users/addresses")
        resp.raise_for_status()
        return resp.json().get("data", resp.json())

    async def add_address(self, address_data: Dict[str, Any]) -> Dict[str, Any]:
        resp = await self._client.post("/api/v1/users/addresses", json=address_data)
        resp.raise_for_status()
        return resp.json().get("data", resp.json())

    async def delete_address(self, address_id: str) -> bool:
        resp = await self._client.delete(f"/api/v1/users/addresses/{address_id}")
        resp.raise_for_status()
        return True
""")

    write_file(f"{pkg_py}/analytics.py", """import httpx
from typing import Dict, Any, Optional

class AnalyticsApi:
    def __init__(self, client: httpx.AsyncClient):
        self._client = client

    async def track_event(self, event_name: str, properties: Dict[str, Any], user_id: Optional[str] = None) -> bool:
        payload = {"eventName": event_name, "properties": properties}
        if user_id: payload["userId"] = user_id
        resp = await self._client.post("/api/v1/analytics/events", json=payload)
        resp.raise_for_status()
        return True

    async def get_summary(self) -> Dict[str, Any]:
        resp = await self._client.get("/api/v1/analytics/summary")
        resp.raise_for_status()
        return resp.json().get("data", resp.json())

    async def get_revenue_rollup(self) -> Dict[str, Any]:
        resp = await self._client.get("/api/v1/analytics/revenue-rollup")
        resp.raise_for_status()
        return resp.json().get("data", resp.json())
""")

    write_file(f"{pkg_py}/notifications.py", """import httpx
from typing import Dict, Any

class NotificationsApi:
    def __init__(self, client: httpx.AsyncClient):
        self._client = client

    async def send_notification(self, recipient: str, channel: str, template: str, data: Dict[str, Any]) -> Dict[str, Any]:
        payload = {
            "recipient": recipient,
            "channel": channel,
            "template": template,
            "data": data
        }
        resp = await self._client.post("/api/v1/notifications/send", json=payload)
        resp.raise_for_status()
        return resp.json().get("data", resp.json())

    async def list_templates(self) -> List[Dict[str, Any]]:
        resp = await self._client.get("/api/v1/notifications/templates")
        resp.raise_for_status()
        return resp.json().get("data", resp.json())
""")

    print("Full enterprise codebase generated.")

if __name__ == "__main__":
    build_full_enterprise_codebase()
