from pydantic import BaseModel, ConfigDict
import datetime

class WorkflowTaskOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    invoice_id: int
    task_type: str
    status: str
    priority: str
    created_at: datetime.datetime
    assigned_to: int | None
    reason: str | None
    due_at: datetime.datetime | None
    completed_at: datetime.datetime | None