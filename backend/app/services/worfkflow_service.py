from app.models.models import WorkflowTasks


def create_workflow_task(
    db,
    invoice_id,
    task_type,
    priority,
    reason
):

    task = WorkflowTasks(
        invoice_id=invoice_id,
        task_type=task_type,
        priority=priority,
        reason=reason
    )

    db.add(task)

    return task