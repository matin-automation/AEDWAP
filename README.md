# AEDWAP

## Problem Statement

Enterprise organizations process large volumes of invoices and other business documents manually.

Employees must extract information from documents, validate data against purchase orders, check business policies, obtain approvals, update enterprise systems, and maintain audit records.

This process is slow, error-prone, and difficult to scale.

This project builds an AI-powered document and workflow automation platform that automates these activities while routing uncertain cases to humans for review.

Schema is 

-- Creating vendors Table 
CREATE TABLE vendors (
    id BIGSERIAL PRIMARY KEY,

    name VARCHAR(255) NOT NULL,

    gst_number VARCHAR(15) UNIQUE,

    email VARCHAR(255),

    phone VARCHAR(20),

    address TEXT,

    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE'
        CHECK (status IN ('ACTIVE', 'INACTIVE')),

    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Creating purchase_orders Table
CREATE TABLE purchase_orders (
    id BIGSERIAL PRIMARY KEY,

    po_number VARCHAR(100) NOT NULL UNIQUE,

    vendor_id BIGINT NOT NULL,

    po_date DATE NOT NULL,

    currency CHAR(3) NOT NULL DEFAULT 'INR',

    subtotal NUMERIC(15,2) NOT NULL
        CHECK (subtotal >= 0),

    tax_amount NUMERIC(15,2) NOT NULL DEFAULT 0
        CHECK (tax_amount >= 0),

    total_amount NUMERIC(15,2) NOT NULL
        CHECK (total_amount >= 0),

    status VARCHAR(20) NOT NULL DEFAULT 'OPEN'
        CHECK (
            status IN (
                'OPEN',
                'CLOSED',
                'CANCELLED'
            )
        ),

    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_purchase_orders_vendor
        FOREIGN KEY (vendor_id)
        REFERENCES vendors(id)
);

-- Creating invoices table

CREATE TABLE invoices (
    id BIGSERIAL PRIMARY KEY,

    invoice_number VARCHAR(100) NOT NULL,

    vendor_id BIGINT NOT NULL,

    purchase_order_id BIGINT,

    invoice_date DATE NOT NULL,

    due_date DATE,

    currency CHAR(3) NOT NULL DEFAULT 'INR',

    subtotal NUMERIC(15,2) NOT NULL
        CHECK (subtotal >= 0),

    tax_amount NUMERIC(15,2) NOT NULL DEFAULT 0
        CHECK (tax_amount >= 0),

    total_amount NUMERIC(15,2) NOT NULL
        CHECK (total_amount >= 0),

    status VARCHAR(30) NOT NULL DEFAULT 'RECEIVED'
        CHECK (
            status IN (
                'RECEIVED',
                'VALIDATING',
                'REVIEW_REQUIRED',
                'PENDING_APPROVAL',
                'APPROVED',
                'REJECTED',
                'PROCESSED'
            )
        ),

    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_invoices_vendor
        FOREIGN KEY (vendor_id)
        REFERENCES vendors(id),

    CONSTRAINT fk_invoices_purchase_order
        FOREIGN KEY (purchase_order_id)
        REFERENCES purchase_orders(id),

    CONSTRAINT unique_vendor_invoice
        UNIQUE (vendor_id, invoice_number)
);

-- creating invoice_items table
CREATE TABLE invoice_items (
    id BIGSERIAL PRIMARY KEY,

    invoice_id BIGINT NOT NULL,

    line_number INTEGER NOT NULL,

    description TEXT NOT NULL,

    product_code VARCHAR(100),

    quantity NUMERIC(15,3) NOT NULL
        CHECK (quantity > 0),

    unit_price NUMERIC(15,2) NOT NULL
        CHECK (unit_price >= 0),

    tax_rate NUMERIC(5,2) NOT NULL DEFAULT 0
        CHECK (tax_rate >= 0 AND tax_rate <= 100),

    total_amount NUMERIC(15,2) NOT NULL
        CHECK (total_amount >= 0),

    CONSTRAINT fk_invoice_items_invoice
        FOREIGN KEY (invoice_id)
        REFERENCES invoices(id)
        ON DELETE CASCADE,

    CONSTRAINT unique_invoice_line
        UNIQUE (invoice_id, line_number)
);

-- creating valuation table


CREATE TABLE validations (
    id BIGSERIAL PRIMARY KEY,

    invoice_id BIGINT NOT NULL,

    validation_type VARCHAR(50) NOT NULL,

    status VARCHAR(20) NOT NULL
        CHECK (
            status IN (
                'PASS',
                'FAIL'
            )
        ),

    expected_value TEXT,

    actual_value TEXT,

    difference NUMERIC(15,2),

    message TEXT NOT NULL,

    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_validations_invoice
        FOREIGN KEY (invoice_id)
        REFERENCES invoices(id)
        ON DELETE CASCADE
);

-- Creating workflow_tasks table

CREATE TABLE workflow_tasks (
    id BIGSERIAL PRIMARY KEY,

    invoice_id BIGINT NOT NULL,

    task_type VARCHAR(50) NOT NULL,

    assigned_to BIGINT,

    status VARCHAR(30) NOT NULL DEFAULT 'PENDING'
        CHECK (
            status IN (
                'PENDING',
                'IN_PROGRESS',
                'COMPLETED',
                'REJECTED',
                'CANCELLED'
            )
        ),

    priority VARCHAR(20) NOT NULL DEFAULT 'MEDIUM'
        CHECK (
            priority IN (
                'LOW',
                'MEDIUM',
                'HIGH',
                'URGENT'
            )
        ),

    reason TEXT,

    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    due_at TIMESTAMPTZ,

    completed_at TIMESTAMPTZ,

    CONSTRAINT fk_workflow_tasks_invoice
        FOREIGN KEY (invoice_id)
        REFERENCES invoices(id)
        ON DELETE CASCADE
);

-- Creating approvals table

CREATE TABLE approvals (
    id BIGSERIAL PRIMARY KEY,

    task_id BIGINT NOT NULL,

    decision VARCHAR(20) NOT NULL
        CHECK (
            decision IN (
                'APPROVED',
                'REJECTED'
            )
        ),

    approved_by BIGINT,

    comment TEXT,

    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_approvals_task
        FOREIGN KEY (task_id)
        REFERENCES workflow_tasks(id)
        ON DELETE CASCADE
);

-- creating audit_log tables

CREATE TABLE audit_logs (
    id BIGSERIAL PRIMARY KEY,

    invoice_id BIGINT NOT NULL,

    action VARCHAR(100) NOT NULL,

    actor_type VARCHAR(20) NOT NULL
        CHECK (
            actor_type IN (
                'USER',
                'SYSTEM'
            )
        ),

    actor_id BIGINT,

    old_value TEXT,

    new_value TEXT,

    details TEXT,

    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_audit_logs_invoice
        FOREIGN KEY (invoice_id)
        REFERENCES invoices(id)
        ON DELETE CASCADE
);

-- Creating necessary Indexes for fast searches 

CREATE INDEX idx_purchase_orders_vendor
    ON purchase_orders(vendor_id);

CREATE INDEX idx_invoices_vendor
    ON invoices(vendor_id);

CREATE INDEX idx_invoices_purchase_order
    ON invoices(purchase_order_id);

CREATE INDEX idx_invoices_status
    ON invoices(status);

CREATE INDEX idx_invoice_items_invoice
    ON invoice_items(invoice_id);

CREATE INDEX idx_validations_invoice
    ON validations(invoice_id);

CREATE INDEX idx_workflow_tasks_invoice
    ON workflow_tasks(invoice_id);

CREATE INDEX idx_workflow_tasks_status
    ON workflow_tasks(status);

CREATE INDEX idx_approvals_task
    ON approvals(task_id);

CREATE INDEX idx_audit_logs_invoice
    ON audit_logs(invoice_id);

CREATE INDEX idx_audit_logs_created_at
    ON audit_logs(created_at);