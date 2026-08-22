from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import InvoiceItems
from app.schemas.invoice_item import InvoiceItemOut

router = APIRouter(prefix="/invoice-items", tags=["invoice_items"])

@router.get("/", response_model=list[InvoiceItemOut])
def list_invoice_items(db: Session = Depends(get_db)):
    return db.query(InvoiceItems).all()

@router.get("/{item_id}", response_model=InvoiceItemOut)
def get_invoice_item(item_id: int, db: Session = Depends(get_db)):
    item = db.get(InvoiceItems, item_id)
    if not item:
        raise HTTPException(404, "invoice item not found")
    return item