from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.models import InvoiceItems
from app.schema.invoice_item import (
    InvoiceItemCreate,
    InvoiceItemResponse
)


router = APIRouter(
    prefix="/invoice-items",
    tags=["Invoice Items"]
)

@router.post("/", response_model=list[InvoiceItemResponse])
def create_invoice_item(
    invoice_items: list[InvoiceItemCreate],  # Renamed to plural for clarity
    db: Session = Depends(get_db)
):
    # Convert each item in the list into a database model instance
    new_items = [
        InvoiceItems(
            invoice_id=item.invoice_id,
            line_number=item.line_number,
            description=item.description,
            quantity=item.quantity,
            unit_price=item.unit_price,
            tax_rate=item.tax_rate,
            total_amount=item.total_amount,
            product_code=item.product_code
        )
        for item in invoice_items
    ]

    # Save all items to the database at once
    db.add_all(new_items)
    db.commit()

    # Refresh each item to populate auto-generated fields (like IDs)
    for item in new_items:
        db.refresh(item)

    return new_items

@router.get("/", response_model=list[InvoiceItemResponse])
def get_invoice_items(
    db: Session = Depends(get_db)
):
    return db.query(InvoiceItems).all()