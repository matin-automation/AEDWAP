from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class ActorType(str, Enum):
    USER = "USER"
    SYSTEM = "SYSTEM"


class AuditLogCreate(BaseModel):
    invoice_id: int
    action: str
    actor_type: ActorType
    actor_id: Optional[int] = None
    old_value: Optional[str] = None
    new_value: Optional[str] = None
    details: Optional[str] = None


class AuditLogResponse(BaseModel):
    id: int
    invoice_id: int
    action: str
    actor_type: ActorType
    created_at: datetime
    actor_id: Optional[int] = None
    old_value: Optional[str] = None
    new_value: Optional[str] = None
    details: Optional[str] = None

    model_config = {
        "from_attributes": True
    }