from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.models import Validations
from app.schema.validation import (
    ValidationCreate,
    ValidationResponse
)


router = APIRouter(
    prefix="/validations",
    tags=["Validations"]
)


@router.post("/", response_model=ValidationResponse)
def create_validation(
    validation: ValidationCreate,
    db: Session = Depends(get_db)
):

    new_validation = Validations(
        invoice_id=validation.invoice_id,
        validation_type=validation.validation_type,
        status=validation.status,
        message=validation.message,
        expected_value=validation.expected_value,
        actual_value=validation.actual_value,
        difference=validation.difference
    )

    db.add(new_validation)
    db.commit()
    db.refresh(new_validation)

    return new_validation


@router.get("/", response_model=list[ValidationResponse])
def get_validations(
    db: Session = Depends(get_db)
):
    return db.query(Validations).all()