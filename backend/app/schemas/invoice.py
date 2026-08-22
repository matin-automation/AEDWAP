from pydantic import BaseModel, ConfigDict
import datetime, decimal

class InvoiceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    invoice_number: str
    vendor_id: int
    invoice_date: datetime.date
    currency: str
    subtotal: decimal.Decimal
    tax_amount: decimal.Decimal
    total_amount: decimal.Decimal
    status: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    purchase_order_id: int | None
    due_date: datetime.date | None