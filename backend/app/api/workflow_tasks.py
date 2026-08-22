from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import WorkflowTasks
from app.schemas.workflow_task import WorkflowTaskOut

router = APIRouter(prefix="/workflow-tasks", tags=["workflow_tasks"])

@router.get("/", response_model=list[WorkflowTaskOut])
def list_workflow_tasks(db: Session = Depends(get_db)):
    return db.query(WorkflowTasks).all()

@router.get("/{task_id}", response_model=WorkflowTaskOut)
def get_workflow_task(task_id: int, db: Session = Depends(get_db)):
    task = db.get(WorkflowTasks, task_id)
    if not task:
        raise HTTPException(404, "workflow task not found")
    return task