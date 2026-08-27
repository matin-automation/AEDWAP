from fastapi import APIRouter, Depends
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


@router.post("/", response_model=WorkflowTaskResponse)
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


@router.get("/", response_model=list[WorkflowTaskResponse])
def get_workflow_tasks(
    db: Session = Depends(get_db)
):
    return db.query(WorkflowTasks).all()