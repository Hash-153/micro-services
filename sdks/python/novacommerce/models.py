from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum
from datetime import datetime

class Currency(str, Enum):
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    CAD = "CAD"
    AUD = "AUD"
    JPY = "JPY"

class Money(BaseModel):
    amount: int
    currency: Currency = Currency.USD

class User(BaseModel):
    id: str
    email: str
    role: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class Product(BaseModel):
    id: str
    sku: str
    name: str
    slug: str
    description: str
    category_id: str
    base_price: Money
    is_active: bool = True
    tags: List[str] = []

class OrderItem(BaseModel):
    sku: str
    quantity: int

class Order(BaseModel):
    id: str
    order_number: str
    user_id: str
    status: str
    subtotal_amount: Money
    tax_amount: Money
    total_amount: Money
    items: List[Dict[str, Any]] = []
    created_at: Optional[datetime] = None
