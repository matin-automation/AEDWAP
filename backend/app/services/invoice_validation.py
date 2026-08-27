from decimal import Decimal

from app.models.models import Invoices


def validate_invoice_amounts(
    subtotal: Decimal,
    tax_amount: Decimal,
    total_amount: Decimal
):
    expected_total = subtotal + tax_amount
    difference = total_amount - expected_total

    if difference == Decimal("0"):
        return {
            "status": "PASS",
            "message": "Invoice total is correct.",
            "expected_value": str(expected_total),
            "actual_value": str(total_amount),
            "difference": difference
        }

    return {
        "status": "FAIL",
        "message": "Invoice total does not equal subtotal plus tax.",
        "expected_value": str(expected_total),
        "actual_value": str(total_amount),
        "difference": difference
    }


def check_duplicate_invoice(
    db,
    vendor_id: int,
    invoice_number: str,
    current_invoice_id=None
):

    query = db.query(Invoices).filter(
        Invoices.vendor_id == vendor_id,
        Invoices.invoice_number == invoice_number
    )

    if current_invoice_id:
        query = query.filter(Invoices.id != current_invoice_id)

    return query.first() is not None