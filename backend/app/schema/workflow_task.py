from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class WorkflowTaskCreate(BaseModel):

    invoice_id: int

    task_type: str

    assigned_to: Optional[int] = None

    reason: Optional[str] = None

    due_at: Optional[datetime] = None


class WorkflowTaskResponse(BaseModel):

    id: int

    invoice_id: int

    task_type: str

    status: str

    priority: str

    created_at: datetime

    assigned_to: Optional[int] = None

    reason: Optional[str] = None

    due_at: Optional[datetime] = None

    completed_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }