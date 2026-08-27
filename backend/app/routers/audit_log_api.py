from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.models import AuditLogs
from app.schema.audit_log import (
    AuditLogCreate,
    AuditLogResponse
)


router = APIRouter(
    prefix="/audit-logs",
    tags=["Audit Logs"]
)


@router.post("/", response_model=AuditLogResponse)
def create_audit_log(
    audit_log: AuditLogCreate,
    db: Session = Depends(get_db)
):

    new_audit_log = AuditLogs(
        invoice_id=audit_log.invoice_id,
        action=audit_log.action,
        actor_type=audit_log.actor_type,
        actor_id=audit_log.actor_id,
        old_value=audit_log.old_value,
        new_value=audit_log.new_value,
        details=audit_log.details
    )

    db.add(new_audit_log)
    db.commit()
    db.refresh(new_audit_log)

    return new_audit_log


@router.get("/", response_model=list[AuditLogResponse])
def get_audit_logs(
    db: Session = Depends(get_db)
):
    return db.query(AuditLogs).all()