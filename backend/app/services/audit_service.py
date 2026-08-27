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
    """
    Create an audit log for an invoice action.

    The function only adds the audit record to the current
    database transaction. The caller decides when to commit.
    """

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
    return audit_log