from pydantic import BaseModel,Field
from datetime import date
from decimal import Decimal

class PurchaseOrderCreate(BaseModel):
    po_number : str
    vendor_id : int
    po_date : date
    currency : str = "INR"
    subtotal : Decimal = Field(ge=0)
    tax_amount : Decimal = Field(default=Decimal("0"),ge=0)
    total_amount : Decimal = Field(ge=0)

class PurchaseOrderResponse(BaseModel):
    id : int
    po_number : str
    vendor_id : int
    po_date : date
    currency: str
    subtotal: Decimal
    tax_amount: Decimal
    total_amount: Decimal
    status: str
    model_config = {
        "from_attributes": True
    }


