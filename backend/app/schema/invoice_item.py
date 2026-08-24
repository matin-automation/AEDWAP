from pydantic import BaseModel, Field
from decimal import Decimal
from typing import Optional


class InvoiceItemCreate(BaseModel):

    invoice_id: int

    line_number: int

    description: str

    quantity: Decimal = Field(gt=0)

    unit_price: Decimal = Field(ge=0)

    tax_rate: Decimal = Field(default=Decimal("0"), ge=0, le=100)

    total_amount: Decimal = Field(ge=0)

    product_code: Optional[str] = None


class InvoiceItemResponse(BaseModel):

    id: int

    invoice_id: int

    line_number: int

    description: str

    quantity: Decimal

    unit_price: Decimal

    tax_rate: Decimal

    total_amount: Decimal

    product_code: Optional[str] = None

    model_config = {
        "from_attributes": True
    }