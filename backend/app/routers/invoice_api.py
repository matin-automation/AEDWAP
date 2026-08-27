from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schema.invoice import InvoiceResponse, InvoiceCreate
from app.core.database import get_db
from app.models.models import Invoices

from app.services.invoice_processing import process_invoice


router = APIRouter(
    prefix="/invoices",
    tags=["Invoices"]
)


@router.get("/", response_model=list[InvoiceResponse])
def get_invoices(
    db: Session = Depends(get_db)
):
    return db.query(Invoices).all()


@router.post("/", response_model=InvoiceResponse)
def create_invoice(
    invoice: InvoiceCreate,
    db: Session = Depends(get_db)
):
    return process_invoice(db, invoice)

## For testing in postman 

# @router.post("/", response_model=InvoiceResponse)
# def create_invoice(
#     invoice: InvoiceCreate,
#     db: Session = Depends(get_db)
# ):

#     new_invoice = Invoices(
#         invoice_number=invoice.invoice_number,
#         vendor_id=invoice.vendor_id,
#         purchase_order_id=invoice.purchase_order_id,
#         invoice_date=invoice.invoice_date,
#         due_date=invoice.due_date,
#         currency=invoice.currency,
#         subtotal=invoice.subtotal,
#         tax_amount=invoice.tax_amount,
#         total_amount=invoice.total_amount
#     )

#     db.add(new_invoice)
#     db.commit()
#     db.refresh(new_invoice)

#     return new_invoice


