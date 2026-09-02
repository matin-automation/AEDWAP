from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.models import WorkflowTasks

from app.schema.workflow_task import (
    WorkflowTaskCreate,
    WorkflowTaskResponse
)


router = APIRouter(
    prefix="/workflow-tasks",
    tags=["Workflow Tasks"]
)


# =========================================================
# 1. CREATE WORKFLOW TASK
# =========================================================

@router.post(
    "/",
    response_model=WorkflowTaskResponse
)
def create_workflow_task(
    workflow_task: WorkflowTaskCreate,
    db: Session = Depends(get_db)
):

    new_workflow_task = WorkflowTasks(
        invoice_id=workflow_task.invoice_id,
        task_type=workflow_task.task_type,
        assigned_to=workflow_task.assigned_to,
        reason=workflow_task.reason,
        due_at=workflow_task.due_at
    )

    db.add(new_workflow_task)
    db.commit()
    db.refresh(new_workflow_task)

    return new_workflow_task


# =========================================================
# 2. GET ALL WORKFLOW TASKS
# =========================================================

@router.get(
    "/",
    response_model=list[WorkflowTaskResponse]
)
def get_workflow_tasks(
    db: Session = Depends(get_db)
):

    return (
        db.query(WorkflowTasks)
        .order_by(WorkflowTasks.created_at.desc())
        .all()
    )


# =========================================================
# 3. GET ONE WORKFLOW TASK
# =========================================================

@router.get(
    "/{task_id}",
    response_model=WorkflowTaskResponse
)
def get_workflow_task(
    task_id: int,
    db: Session = Depends(get_db)
):

    task = (
        db.query(WorkflowTasks)
        .filter(WorkflowTasks.id == task_id)
        .first()
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Workflow task not found."
        )

    return task


# =========================================================
# 4. ASSIGN WORKFLOW TASK
# =========================================================

@router.post(
    "/{task_id}/assign"
)
def assign_workflow_task(
    task_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):

    task = (
        db.query(WorkflowTasks)
        .filter(WorkflowTasks.id == task_id)
        .first()
    )

    # -----------------------------------------------------
    # Task does not exist
    # -----------------------------------------------------

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Workflow task not found."
        )

    # -----------------------------------------------------
    # Only pending tasks can be assigned
    # -----------------------------------------------------

    if task.status != "PENDING":
        raise HTTPException(
            status_code=400,
            detail=(
                f"Task cannot be assigned because its "
                f"current status is {task.status}."
            )
        )

    # -----------------------------------------------------
    # Assign reviewer
    # -----------------------------------------------------

    task.assigned_to = user_id

    # -----------------------------------------------------
    # Move task into progress
    # -----------------------------------------------------

    task.status = "IN_PROGRESS"

    db.commit()
    db.refresh(task)

    return {
        "message": "Workflow task assigned successfully.",
        "task_id": task.id,
        "assigned_to": task.assigned_to,
        "status": task.status
    }

