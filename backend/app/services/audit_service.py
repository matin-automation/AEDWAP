from sqlalchemy.orm import Session

from app.models.models import AuditLogs


def create_audit_log(
    db: Session,
    invoice_id: int,
    action: str,
    actor_type: str,
    actor_id: int | None = None,
    old_value: str | None = None,
    new_value: str | None = None,
    details: str | None = None,
):
    audit_log = AuditLogs(
        invoice_id=invoice_id,
        action=action,
        actor_type=actor_type,
        actor_id=actor_id,
        old_value=old_value,
        new_value=new_value,
        details=details,
    )

    db.add(audit_log)
    db.commit()
    db.refresh(audit_log)

    return audit_log