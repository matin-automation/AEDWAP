from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import PurchaseOrders
from app.schemas.purchase_order import PurchaseOrderOut

router = APIRouter(prefix="/purchase-orders", tags=["purchase_orders"])

@router.get("/", response_model=list[PurchaseOrderOut])
def list_purchase_orders(db: Session = Depends(get_db)):
    return db.query(PurchaseOrders).all()

@router.get("/{po_id}", response_model=PurchaseOrderOut)
def get_purchase_order(po_id: int, db: Session = Depends(get_db)):
    po = db.get(PurchaseOrders, po_id)
    if not po:
        raise HTTPException(404, "purchase order not found")
    return po