def determine_workflow(
    amount_validation,
    po_validation
):

# Amount validation failed
    if amount_validation["status"] == "FAIL":
        return {
            "invoice_status": "REVIEW_REQUIRED",
            "task_type": "AMOUNT_MISMATCH_REVIEW",
            "priority": "HIGH",
            "reason": amount_validation["message"]
        }

 # PO validation failed
    if po_validation["status"] == "FAIL":

        return {
            "invoice_status": "REVIEW_REQUIRED",
            "task_type": "PO_MATCH_REVIEW",
            "priority": "HIGH",
            "reason": po_validation["reason"]
        }

# Everything passed
    return {
        "invoice_status": "PENDING_APPROVAL",
        "task_type": "MANAGER_APPROVAL",
        "priority": "MEDIUM",
        "reason": "Invoice passed automated validation."
    }