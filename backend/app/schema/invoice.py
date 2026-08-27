from pydantic import BaseModel,Field
from datetime import date
from decimal import Decimal
from typing import Optional

class InvoiceCreate(BaseModel):
    invoice_number : str=Field(max_length=100)
    vendor_id : int
    purchase_order_id: Optional[int] = None
    invoice_date : date
    due_date: Optional[date] = None
    currency : str=Field(default="INR",max_length=3)
    subtotal : Decimal= Field(default=Decimal("0"),ge=0)
    tax_amount : Decimal= Field(default=Decimal("0"),ge=0)
    total_amount : Decimal= Field(default=Decimal("0"),ge=0)

class InvoiceResponse(BaseModel):
    id : int
    invoice_number : str
    vendor_id : int
    purchase_order_id: Optional[int] = None
    invoice_date : date
    due_date: Optional[date] = None
    currency : str
    subtotal : Decimal
    tax_amount : Decimal
    total_amount : Decimal
    status : str
    model_config = {
        "from_attributes" : True
    }

