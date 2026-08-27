from decimal import Decimal

from app.models.models import PurchaseOrders


def match_invoice_with_po(
    db,
    invoice
):

    if invoice.purchase_order_id is None:
        return {
            "status": "FAIL",
            "reason": "Invoice does not have a purchase order."
        }

    po = db.query(PurchaseOrders).filter(
        PurchaseOrders.id == invoice.purchase_order_id
    ).first()

    if not po:
        return {
            "status": "FAIL",
            "reason": "Purchase order does not exist."
        }

    if invoice.vendor_id != po.vendor_id:
        return {
            "status": "FAIL",
            "reason": "Invoice vendor does not match purchase order vendor."
        }

    if invoice.currency != po.currency:
        return {
            "status": "FAIL",
            "reason": "Invoice currency does not match purchase order currency."
        }

    difference = invoice.total_amount - po.total_amount

    if difference != Decimal("0"):
        return {
            "status": "FAIL",
            "reason": "Invoice total does not match purchase order total.",
            "expected_value": str(po.total_amount),
            "actual_value": str(invoice.total_amount),
            "difference": difference
        }

    return {
        "status": "PASS",
        "reason": "Invoice matches purchase order."
    }