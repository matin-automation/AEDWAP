from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import Approvals
from app.schemas.approval import ApprovalOut

router = APIRouter(prefix="/approvals", tags=["approvals"])

@router.get("/", response_model=list[ApprovalOut])
def list_approvals(db: Session = Depends(get_db)):
    return db.query(Approvals).all()

@router.get("/{approval_id}", response_model=ApprovalOut)
def get_approval(approval_id: int, db: Session = Depends(get_db)):
    a = db.get(Approvals, approval_id)
    if not a:
        raise HTTPException(404, "approval not found")
    return a