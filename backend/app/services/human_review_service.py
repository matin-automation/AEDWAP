from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.models import (
    Invoices,
    WorkflowTasks,
    Approvals,
)

from app.services.audit_service import create_audit_log


def approve_workflow_task(
    db: Session,
    task_id: int,
    approved_by: int | None = None,
    comment: str | None = None,
):
    """
    Approve a pending workflow task.

    Updates:
    - Workflow task
    - Invoice
    - Approval record
    - Audit log
    """

    # ---------------------------------------------------------
    # 1. Find workflow task
    # ---------------------------------------------------------

    task = (
        db.query(WorkflowTasks)
        .filter(WorkflowTasks.id == task_id)
        .first()
    )

    if task is None:
        return {
            "error": "Workflow task not found."
        }

    # ---------------------------------------------------------
    # 2. Check task status
    # ---------------------------------------------------------

    if task.status != "PENDING":
        return {
            "error": f"Task cannot be approved because its current status is {task.status}."
        }

    # ---------------------------------------------------------
    # 3. Find invoice
    # ---------------------------------------------------------

    invoice = (
        db.query(Invoices)
        .filter(Invoices.id == task.invoice_id)
        .first()
    )

    if invoice is None:
        return {
            "error": "Invoice not found."
        }

    # ---------------------------------------------------------
    # 4. Store old invoice status
    # ---------------------------------------------------------

    old_invoice_status = invoice.status

    # ---------------------------------------------------------
    # 5. Update invoice
    # ---------------------------------------------------------

    invoice.status = "APPROVED"

    # ---------------------------------------------------------
    # 6. Complete workflow task
    # ---------------------------------------------------------

    task.status = "COMPLETED"
    task.completed_at = datetime.now(timezone.utc)

    # ---------------------------------------------------------
    # 7. Create approval record
    # ---------------------------------------------------------

    approval = Approvals(
        task_id=task.id,
        decision="APPROVED",
        approved_by=approved_by,
        comment=comment,
    )

    db.add(approval)

    # ---------------------------------------------------------
    # 8. Create audit log
    # ---------------------------------------------------------

    create_audit_log(
        db=db,
        invoice_id=invoice.id,
        action="INVOICE_APPROVED",
        actor_type="USER",
        actor_id=approved_by,
        old_value=old_invoice_status,
        new_value="APPROVED",
        details=comment or "Invoice approved by human reviewer.",
    )

    # ---------------------------------------------------------
    # 9. Commit everything together
    # ---------------------------------------------------------

    db.commit()

    db.refresh(invoice)
    db.refresh(task)
    db.refresh(approval)

    return {
        "message": "Invoice approved successfully.",
        "invoice_id": invoice.id,
        "task_id": task.id,
        "invoice_status": invoice.status,
        "task_status": task.status,
        "decision": approval.decision,
    }


def reject_workflow_task(
    db: Session,
    task_id: int,
    approved_by: int | None = None,
    comment: str | None = None,
):
    """
    Reject a pending workflow task.

    Updates:
    - Workflow task
    - Invoice
    - Approval record
    - Audit log
    """

    # ---------------------------------------------------------
    # 1. Find workflow task
    # ---------------------------------------------------------

    task = (
        db.query(WorkflowTasks)
        .filter(WorkflowTasks.id == task_id)
        .first()
    )

    if task is None:
        return {
            "error": "Workflow task not found."
        }

    # ---------------------------------------------------------
    # 2. Check task status
    # ---------------------------------------------------------

    if task.status != "PENDING":
        return {
            "error": f"Task cannot be rejected because its current status is {task.status}."
        }

    # ---------------------------------------------------------
    # 3. Find invoice
    # ---------------------------------------------------------

    invoice = (
        db.query(Invoices)
        .filter(Invoices.id == task.invoice_id)
        .first()
    )

    if invoice is None:
        return {
            "error": "Invoice not found."
        }

    # ---------------------------------------------------------
    # 4. Store old status
    # ---------------------------------------------------------

    old_invoice_status = invoice.status

    # ---------------------------------------------------------
    # 5. Update invoice
    # ---------------------------------------------------------

    invoice.status = "REJECTED"

    # ---------------------------------------------------------
    # 6. Update workflow task
    # ---------------------------------------------------------

    task.status = "REJECTED"
    task.completed_at = datetime.now(timezone.utc)

    # ---------------------------------------------------------
    # 7. Create approval/rejection record
    # ---------------------------------------------------------

    approval = Approvals(
        task_id=task.id,
        decision="REJECTED",
        approved_by=approved_by,
        comment=comment,
    )

    db.add(approval)

    # ---------------------------------------------------------
    # 8. Create audit log
    # ---------------------------------------------------------

    create_audit_log(
        db=db,
        invoice_id=invoice.id,
        action="INVOICE_REJECTED",
        actor_type="USER",
        actor_id=approved_by,
        old_value=old_invoice_status,
        new_value="REJECTED",
        details=comment or "Invoice rejected by human reviewer.",
    )

    # ---------------------------------------------------------
    # 9. Commit everything
    # ---------------------------------------------------------

    db.commit()

    db.refresh(invoice)
    db.refresh(task)
    db.refresh(approval)

    return {
        "message": "Invoice rejected successfully.",
        "invoice_id": invoice.id,
        "task_id": task.id,
        "invoice_status": invoice.status,
        "task_status": task.status,
        "decision": approval.decision,
    }