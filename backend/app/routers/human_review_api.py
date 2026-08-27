from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.human_review_service import (
    approve_workflow_task,
    reject_workflow_task,
)


router = APIRouter(
    prefix="/human-review",
    tags=["Human Review"],
)


@router.post("/{task_id}/approve")
def approve_task(
    task_id: int,
    db: Session = Depends(get_db),
):
    result = approve_workflow_task(
        db=db,
        task_id=task_id,
    )

    if "error" in result:
        raise HTTPException(
            status_code=404,
            detail=result["error"],
        )

    return result


@router.post("/{task_id}/reject")
def reject_task(
    task_id: int,
    db: Session = Depends(get_db),
):
    result = reject_workflow_task(
        db=db,
        task_id=task_id,
    )

    if "error" in result:
        raise HTTPException(
            status_code=404,
            detail=result["error"],
        )

    return result