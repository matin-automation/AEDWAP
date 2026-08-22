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