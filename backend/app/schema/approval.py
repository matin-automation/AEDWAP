from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class ApprovalDecision(str, Enum):
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class ApprovalCreate(BaseModel):
    task_id: int
    decision: ApprovalDecision
    approved_by: Optional[int] = None
    comment: Optional[str] = None


class ApprovalResponse(BaseModel):
    id: int
    task_id: int
    decision: ApprovalDecision
    created_at: datetime
    approved_by: Optional[int] = None
    comment: Optional[str] = None

    model_config = {
        "from_attributes": True
    }