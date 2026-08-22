from pydantic import BaseModel, ConfigDict
import datetime, decimal

class PurchaseOrderOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    po_number: str
    vendor_id: int
    po_date: datetime.date
    currency: str
    subtotal: decimal.Decimal
    tax_amount: decimal.Decimal
    total_amount: decimal.Decimal
    status: str
    created_at: datetime.datetime
    updated_at: datetime.datetime