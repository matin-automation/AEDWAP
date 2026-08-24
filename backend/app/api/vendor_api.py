from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.models import Vendors
from app.schema.vendor import VendorCreate, VendorResponse


router = APIRouter(
    prefix="/vendors",
    tags=["Vendors"]
)


@router.post("/", response_model=VendorResponse)
def create_vendor(
    vendor: VendorCreate,
    db: Session = Depends(get_db)
):
    new_vendor = Vendors(
        name=vendor.name,
        gst_number=vendor.gst_number,
        email=vendor.email,
        phone=vendor.phone,
        address=vendor.address
    )

    db.add(new_vendor)
    db.commit()
    db.refresh(new_vendor)

    return new_vendor


@router.get("/", response_model=list[VendorResponse])
def get_vendors(db: Session = Depends(get_db)):
    return db.query(Vendors).all()