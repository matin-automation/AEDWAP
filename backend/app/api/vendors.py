from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import Vendors
from app.schemas.vendor import VendorOut

router = APIRouter(prefix="/vendors", tags=["vendors"])

@router.get("/", response_model=list[VendorOut])
def list_vendors(db: Session = Depends(get_db)):
    return db.query(Vendors).all()

@router.get("/{vendor_id}", response_model=VendorOut)
def get_vendor(vendor_id: int, db: Session = Depends(get_db)):
    vendor = db.get(Vendors, vendor_id)
    if not vendor:
        raise HTTPException(404, "vendor not found")
    return vendor