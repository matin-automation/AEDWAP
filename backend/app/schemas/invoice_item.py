from pydantic import BaseModel, ConfigDict
import decimal

class InvoiceItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    invoice_id: int
    line_number: int
    description: str
    quantity: decimal.Decimal
    unit_price: decimal.Decimal
    tax_rate: decimal.Decimal
    total_amount: decimal.Decimal
    product_code: str | None