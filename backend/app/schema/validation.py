from pydantic import BaseModel
from typing import Optional
from decimal import Decimal


class ValidationCreate(BaseModel):

    invoice_id: int

    validation_type: str

    status: str

    message: str

    expected_value: Optional[str] = None

    actual_value: Optional[str] = None

    difference: Optional[Decimal] = None


class ValidationResponse(BaseModel):

    id: int

    invoice_id: int

    validation_type: str

    status: str

    message: str

    expected_value: Optional[str] = None

    actual_value: Optional[str] = None

    difference: Optional[Decimal] = None

    model_config = {
        "from_attributes": True
    }