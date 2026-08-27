from decimal import Decimal


# ---------------------------------------------------------
# Non-PO invoice policy limit
# ---------------------------------------------------------

MAX_NON_PO_AMOUNT = Decimal("10000.00")


def evaluate_non_po_invoice(invoice):
    """
    Evaluate an invoice that does not have a Purchase Order.

    Returns:
        status   -> validation result (PASS / FAIL)
        decision -> workflow decision
        priority -> workflow priority
        reason   -> explanation
    """

    # ---------------------------------------------------------
    # 1. PO exists
    # ---------------------------------------------------------

    if invoice.purchase_order_id is not None:
        return {
            "status": "PASS",
            "decision": "PROCESS_WITH_PO",
            "priority": "MEDIUM",
            "reason": "Invoice has a Purchase Order."
        }

    # ---------------------------------------------------------
    # 2. Invoice amount is missing
    # ---------------------------------------------------------

    if invoice.total_amount is None:
        return {
            "status": "FAIL",
            "decision": "HUMAN_REVIEW",
            "priority": "HIGH",
            "reason": "Invoice total amount is missing."
        }

    # ---------------------------------------------------------
    # 3. Invoice amount is invalid
    # ---------------------------------------------------------

    if invoice.total_amount <= 0:
        return {
            "status": "FAIL",
            "decision": "HUMAN_REVIEW",
            "priority": "HIGH",
            "reason": "Invoice total amount must be greater than zero."
        }

    # ---------------------------------------------------------
    # 4. High-value Non-PO invoice
    # ---------------------------------------------------------

    if invoice.total_amount > MAX_NON_PO_AMOUNT:
        return {
            "status": "FAIL",
            "decision": "HUMAN_REVIEW",
            "priority": "HIGH",
            "reason": (
                f"Non-PO invoice exceeds the permitted "
                f"amount limit of ₹{MAX_NON_PO_AMOUNT}."
            )
        }

    # ---------------------------------------------------------
    # 5. Normal Non-PO invoice
    # ---------------------------------------------------------

    return {
        "status": "PASS",
        "decision": "HUMAN_REVIEW",
        "priority": "MEDIUM",
        "reason": (
            "Non-PO invoice requires human review "
            "according to Non-PO policy."
        )
    }



# def evaluate_non_po_invoice(invoice):
#     """
#     Evaluate a Non-PO invoice.

#     Business rule:
#     - Every Non-PO invoice requires human review.
#     - The amount determines the review reason/priority.
#     """

#     # 1. PO exists → Non-PO policy is not applicable
#     if invoice.purchase_order_id is not None:
#         return {
#             "status": "NOT_APPLICABLE",
#             "decision": "PROCESS_WITH_PO",
#             "priority": "MEDIUM",
#             "reason": "Invoice has a Purchase Order."
#         }

#     # 2. Missing invoice amount
#     if invoice.total_amount is None:
#         return {
#             "status": "FAIL",
#             "decision": "HUMAN_REVIEW",
#             "priority": "URGENT",
#             "reason": "Invoice total amount is missing."
#         }

#     # 3. Invalid invoice amount
#     if invoice.total_amount <= 0:
#         return {
#             "status": "FAIL",
#             "decision": "HUMAN_REVIEW",
#             "priority": "URGENT",
#             "reason": "Invoice total amount must be greater than zero."
#         }

#     # 4. High-value Non-PO invoice
#     if invoice.total_amount > 10000:
#         return {
#             "status": "REVIEW_REQUIRED",
#             "decision": "HUMAN_REVIEW",
#             "priority": "HIGH",
#             "reason": (
#                 "Non-PO invoice exceeds ₹10,000 and requires "
#                 "human review."
#             )
#         }

#     # 5. Normal Non-PO invoice
#     return {
#         "status": "REVIEW_REQUIRED",
#         "decision": "HUMAN_REVIEW",
#         "priority": "MEDIUM",
#         "reason": (
#             "Non-PO invoice requires human review "
#             "according to Non-PO policy."
#         )
#     }