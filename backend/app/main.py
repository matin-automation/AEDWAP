<<<<<<< HEAD
from fastapi import FastAPI
from app.api import vendors, purchase_orders, invoices, invoice_items, validations, workflow_tasks, approvals

app = FastAPI(title="AEDWAP")

app.include_router(vendors.router)
app.include_router(purchase_orders.router)
app.include_router(invoices.router)
app.include_router(invoice_items.router)
app.include_router(validations.router)
app.include_router(workflow_tasks.router)
app.include_router(approvals.router)

@app.get("/")
def root():
    return {"status": "ok"}
=======
from fastapi import FastAPI

from app.api.vendor_api import router as vendor_router
from app.api.purchase_order_api import router as purchase_order_router
from app.api.invoice_api import router as invoice_router
from app.api.invoice_item_api import router as invoice_item_router
from app.api.validation_api import router as validation_router
from app.api.workflow_task_api import router as workflow_task_router
from app.api.approval_api import router as approval_router
from app.api.audit_log_api import router as audit_log_router


app = FastAPI(
    title="AEDWAP",
    version="1.0.0",
    description="AI-Powered Enterprise Document & Workflow Automation Platform"
)


app.include_router(vendor_router)
app.include_router(purchase_order_router)
app.include_router(invoice_router)
app.include_router(invoice_item_router)
app.include_router(validation_router)
app.include_router(workflow_task_router)
app.include_router(approval_router)
app.include_router(audit_log_router)
>>>>>>> 9f132266c64013c2075e8e445d55a2a65744e3e4
