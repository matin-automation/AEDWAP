from pydantic import BaseModel, ConfigDict
import datetime, decimal

class ValidationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    invoice_id: int
    validation_type: str
    status: str
    message: str
    created_at: datetime.datetime
    expected_value: str | None
    actual_value: str | None
    difference: decimal.Decimal | None