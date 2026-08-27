from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.models import PurchaseOrders
from app.schema.purchase_order import (
    PurchaseOrderCreate,
    PurchaseOrderResponse
)


router = APIRouter(
    prefix="/purchase-orders",
    tags=["Purchase Orders"]
)


@router.post("/", response_model=PurchaseOrderResponse)
def create_purchase_order(
    purchase_order: PurchaseOrderCreate,
    db: Session = Depends(get_db)
):
    new_purchase_order = PurchaseOrders(
        po_number=purchase_order.po_number,
        vendor_id=purchase_order.vendor_id,
        po_date=purchase_order.po_date,
        currency=purchase_order.currency,
        subtotal=purchase_order.subtotal,
        tax_amount=purchase_order.tax_amount,
        total_amount=purchase_order.total_amount
    )

    db.add(new_purchase_order)
    db.commit()
    db.refresh(new_purchase_order)

    return new_purchase_order

@router.get("/",response_model=list[PurchaseOrderResponse])
def get_purchase_order(db:Session=Depends(get_db)):
    return db.query(PurchaseOrders).all()
