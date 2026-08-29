from typing import Dict, Any, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

class ApiGatewayModelV5Payload(BaseModel):
    id: str = Field(..., description="Unique entity identifier")
    tenant_id: str = Field(..., description="Multi-tenant account identifier")
    entity_code: str = Field(..., description="Alphanumeric business code")
    display_name: str = Field(..., description="Human readable name")
    status: str = Field(default="ACTIVE", description="Operating lifecycle status")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Custom extensible payload attributes")
    version: int = Field(default=1, description="Optimistic locking revision number")
    is_deleted: bool = Field(default=False, description="Soft deletion indicator")
    created_at: Optional[datetime] = Field(default=None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(default=None, description="Last update timestamp")

class ApiGatewayModelV5Filter(BaseModel):
    tenant_id: str
    status: Optional[str] = None
    search: Optional[str] = None
    limit: int = 20
    offset: int = 0

class ApiGatewayModelV5ListResponse(BaseModel):
    items: List[ApiGatewayModelV5Payload]
    total_count: int
    limit: int
    offset: int
    has_more: bool
