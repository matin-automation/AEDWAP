from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import Validations
from app.schemas.validation import ValidationOut

router = APIRouter(prefix="/validations", tags=["validations"])

@router.get("/", response_model=list[ValidationOut])
def list_validations(db: Session = Depends(get_db)):
    return db.query(Validations).all()

@router.get("/{validation_id}", response_model=ValidationOut)
def get_validation(validation_id: int, db: Session = Depends(get_db)):
    v = db.get(Validations, validation_id)
    if not v:
        raise HTTPException(404, "validation not found")
    return v