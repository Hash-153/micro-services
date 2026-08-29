import httpx
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
