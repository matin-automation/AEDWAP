from app.models.models import Invoices, WorkflowTasks

from app.services.invoice_validation import (
    validate_invoice_amounts
)

from app.services.po_matching import (
    match_invoice_with_po
)

from app.services.non_po_policy import (
    evaluate_non_po_invoice
)

from app.services.create_validation_service import (
    create_validation_record
)

from app.services.workflow_engine import (
    determine_workflow
)


def process_invoice(db, invoice):

    # ---------------------------------------------------------
    # 1. Create invoice
    # ---------------------------------------------------------

    new_invoice = Invoices(
        invoice_number=invoice.invoice_number,
        vendor_id=invoice.vendor_id,
        purchase_order_id=invoice.purchase_order_id,
        invoice_date=invoice.invoice_date,
        due_date=invoice.due_date,
        currency=invoice.currency,
        subtotal=invoice.subtotal,
        tax_amount=invoice.tax_amount,
        total_amount=invoice.total_amount
    )

    db.add(new_invoice)

    # Generate invoice ID without committing yet
    db.flush()


    # ---------------------------------------------------------
    # 2. Validate invoice amounts
    # ---------------------------------------------------------

    amount_result = validate_invoice_amounts(
        new_invoice.subtotal,
        new_invoice.tax_amount,
        new_invoice.total_amount
    )

    create_validation_record(
        db,
        new_invoice.id,
        "TOTAL_AMOUNT",
        amount_result
    )


    # ---------------------------------------------------------
    # 3. Process PO / Non-PO invoice
    # ---------------------------------------------------------

    if new_invoice.purchase_order_id is not None:

        # =====================================================
        # PO INVOICE
        # =====================================================

        po_result = match_invoice_with_po(
            db,
            new_invoice
        )

        create_validation_record(
            db,
            new_invoice.id,
            "PO_MATCH",
            po_result
        )

        workflow = determine_workflow(
            amount_result,
            po_result
        )

    else:

        # =====================================================
        # NON-PO INVOICE
        # =====================================================

        non_po_result = evaluate_non_po_invoice(
            new_invoice
        )

        create_validation_record(
            db,
            new_invoice.id,
            "NON_PO_POLICY",
            non_po_result
        )

        workflow = {
            "invoice_status": "REVIEW_REQUIRED",
            "task_type": "NON_PO_REVIEW",
            "priority": "HIGH",
            "reason": non_po_result["reason"]
        }


    # ---------------------------------------------------------
    # 4. Update invoice status
    # ---------------------------------------------------------

    new_invoice.status = workflow["invoice_status"]


    # ---------------------------------------------------------
    # 5. Create workflow task
    # ---------------------------------------------------------

    workflow_task = WorkflowTasks(
        invoice_id=new_invoice.id,
        task_type=workflow["task_type"],
        status="PENDING",
        priority=workflow["priority"],
        reason=workflow["reason"]
    )

    db.add(workflow_task)


    # ---------------------------------------------------------
    # 6. Commit everything
    # ---------------------------------------------------------

    db.commit()

    db.refresh(new_invoice)

    return new_invoice









# from app.models.models import Invoices

# from app.services.invoice_validation import (
#     validate_invoice_amounts
# )

# from app.services.po_matching import (
#     match_invoice_with_po
# )

# from app.services.non_po_policy import (
#     evaluate_non_po_invoice
# )

# from app.services.create_validation_service import (
#     create_validation_record
# )

# from app.services.workflow_engine import (
#     determine_workflow
# )


# def process_invoice(db, invoice):
#     # ---------------------------------------------------------
#     # 1. Create invoice
#     # ---------------------------------------------------------

#     new_invoice = Invoices(
#         invoice_number=invoice.invoice_number,
#         vendor_id=invoice.vendor_id,
#         purchase_order_id=invoice.purchase_order_id,
#         invoice_date=invoice.invoice_date,
#         due_date=invoice.due_date,
#         currency=invoice.currency,
#         subtotal=invoice.subtotal,
#         tax_amount=invoice.tax_amount,
#         total_amount=invoice.total_amount
#     )

#     db.add(new_invoice)
#     db.commit()
#     db.refresh(new_invoice)

#     # ---------------------------------------------------------
#     # 2. Validate invoice amounts
#     # ---------------------------------------------------------

#     amount_result = validate_invoice_amounts(
#         new_invoice.subtotal,
#         new_invoice.tax_amount,
#         new_invoice.total_amount
#     )

#     create_validation_record(
#         db,
#         new_invoice.id,
#         "TOTAL_AMOUNT",
#         amount_result
#     )

#     # ---------------------------------------------------------
#     # 3. Process PO / Non-PO invoice
#     # ---------------------------------------------------------

#     if new_invoice.purchase_order_id is not None:

#         # =====================================================
#         # PO INVOICE
#         # =====================================================

#         po_result = match_invoice_with_po(
#             db,
#             new_invoice
#         )

#         create_validation_record(
#             db,
#             new_invoice.id,
#             "PO_MATCH",
#             po_result
#         )

#         workflow = determine_workflow(
#             amount_result,
#             po_result
#         )

#     else:

#         # =====================================================
#         # NON-PO INVOICE
#         # =====================================================

#         non_po_result = evaluate_non_po_invoice(
#             new_invoice
#         )

#         create_validation_record(
#             db,
#             new_invoice.id,
#             "NON_PO_POLICY",
#             non_po_result
#         )

#         workflow = {
#             "invoice_status": "REVIEW_REQUIRED",
#             "decision": non_po_result["decision"],
#             "priority": non_po_result["priority"],
#             "reason": non_po_result["reason"]
#         }

#     # ---------------------------------------------------------
#     # 4. Update invoice status
#     # ---------------------------------------------------------

#     new_invoice.status = workflow["invoice_status"]

#     db.commit()
#     db.refresh(new_invoice)

#     return new_invoice