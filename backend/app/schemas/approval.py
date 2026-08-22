from pydantic import BaseModel, ConfigDict
import datetime

class ApprovalOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    task_id: int
    decision: str
    created_at: datetime.datetime
    approved_by: int | None
    comment: str | None