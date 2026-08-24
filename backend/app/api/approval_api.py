from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.models import Approvals
from app.schema.approval import (
    ApprovalCreate,
    ApprovalResponse
)


router = APIRouter(
    prefix="/approvals",
    tags=["Approvals"]
)


@router.post("/", response_model=ApprovalResponse)
def create_approval(
    approval: ApprovalCreate,
    db: Session = Depends(get_db)
):

    new_approval = Approvals(
        task_id=approval.task_id,
        decision=approval.decision,
        approved_by=approval.approved_by,
        comment=approval.comment
    )

    db.add(new_approval)
    db.commit()
    db.refresh(new_approval)

    return new_approval


@router.get("/", response_model=list[ApprovalResponse])
def get_approvals(
    db: Session = Depends(get_db)
):
    return db.query(Approvals).all()