from typing import Optional
import datetime
import decimal

from sqlalchemy import BigInteger, CHAR, CheckConstraint, Date, DateTime, ForeignKeyConstraint, Index, Integer, Numeric, PrimaryKeyConstraint, String, Text, UniqueConstraint, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from app.core.database import Base
from sqlalchemy.dialects.postgresql import JSONB
# class Base(DeclarativeBase):
#     pass


class Vendors(Base):
    __tablename__ = 'vendors'
    __table_args__ = (
        CheckConstraint("status::text = ANY (ARRAY['ACTIVE'::character varying, 'INACTIVE'::character varying]::text[])", name='vendors_status_check'),
        PrimaryKeyConstraint('id', name='vendors_pkey'),
        UniqueConstraint('gst_number', name='vendors_gst_number_key')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, server_default=text("'ACTIVE'::character varying"))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    gst_number: Mapped[Optional[str]] = mapped_column(String(15))
    email: Mapped[Optional[str]] = mapped_column(String(255))
    phone: Mapped[Optional[str]] = mapped_column(String(20),unique=True,nullable=False)
    address: Mapped[Optional[str]] = mapped_column(Text)

    purchase_orders: Mapped[list['PurchaseOrders']] = relationship('PurchaseOrders', back_populates='vendor')
    invoices: Mapped[list['Invoices']] = relationship('Invoices', back_populates='vendor')


class PurchaseOrders(Base):
    __tablename__ = 'purchase_orders'
    __table_args__ = (
        CheckConstraint("status::text = ANY (ARRAY['OPEN'::character varying, 'CLOSED'::character varying, 'CANCELLED'::character varying]::text[])", name='purchase_orders_status_check'),
        CheckConstraint('subtotal >= 0::numeric', name='purchase_orders_subtotal_check'),
        CheckConstraint('tax_amount >= 0::numeric', name='purchase_orders_tax_amount_check'),
        CheckConstraint('total_amount >= 0::numeric', name='purchase_orders_total_amount_check'),
        ForeignKeyConstraint(['vendor_id'], ['vendors.id'], name='fk_purchase_orders_vendor'),
        PrimaryKeyConstraint('id', name='purchase_orders_pkey'),
        UniqueConstraint('po_number', name='purchase_orders_po_number_key'),
        Index('idx_purchase_orders_vendor', 'vendor_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    po_number: Mapped[str] = mapped_column(String(100), nullable=False)
    vendor_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    po_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    currency: Mapped[str] = mapped_column(CHAR(3), nullable=False, server_default=text("'INR'::bpchar"))
    subtotal: Mapped[decimal.Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    tax_amount: Mapped[decimal.Decimal] = mapped_column(Numeric(15, 2), nullable=False, server_default=text('0'))
    total_amount: Mapped[decimal.Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, server_default=text("'OPEN'::character varying"))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False, server_default=text('CURRENT_TIMESTAMP'))

    vendor: Mapped['Vendors'] = relationship('Vendors', back_populates='purchase_orders')
    invoices: Mapped[list['Invoices']] = relationship('Invoices', back_populates='purchase_order')


class Invoices(Base):
    __tablename__ = 'invoices'
    __table_args__ = (
        CheckConstraint("status::text = ANY (ARRAY['RECEIVED'::character varying, 'VALIDATING'::character varying, 'REVIEW_REQUIRED'::character varying, 'PENDING_APPROVAL'::character varying, 'APPROVED'::character varying, 'REJECTED'::character varying, 'PROCESSED'::character varying]::text[])", name='invoices_status_check'),
        CheckConstraint('subtotal >= 0::numeric', name='invoices_subtotal_check'),
        CheckConstraint('tax_amount >= 0::numeric', name='invoices_tax_amount_check'),
        CheckConstraint('total_amount >= 0::numeric', name='invoices_total_amount_check'),
        ForeignKeyConstraint(['purchase_order_id'], ['purchase_orders.id'], name='fk_invoices_purchase_order'),
        ForeignKeyConstraint(['vendor_id'], ['vendors.id'], name='fk_invoices_vendor'),
        PrimaryKeyConstraint('id', name='invoices_pkey'),
        UniqueConstraint('vendor_id', 'invoice_number', name='unique_vendor_invoice'),
        Index('idx_invoices_purchase_order', 'purchase_order_id'),
        Index('idx_invoices_status', 'status'),
        Index('idx_invoices_vendor', 'vendor_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    invoice_number: Mapped[str] = mapped_column(String(100), nullable=False)
    vendor_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    invoice_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    currency: Mapped[str] = mapped_column(CHAR(3), nullable=False, server_default=text("'INR'::bpchar"))
    subtotal: Mapped[decimal.Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    tax_amount: Mapped[decimal.Decimal] = mapped_column(Numeric(15, 2), nullable=False, server_default=text('0'))
    total_amount: Mapped[decimal.Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False, server_default=text("'RECEIVED'::character varying"))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    purchase_order_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    due_date: Mapped[Optional[datetime.date]] = mapped_column(Date)

    purchase_order: Mapped[Optional['PurchaseOrders']] = relationship('PurchaseOrders', back_populates='invoices')
    vendor: Mapped['Vendors'] = relationship('Vendors', back_populates='invoices')
    audit_logs: Mapped[list['AuditLogs']] = relationship('AuditLogs', back_populates='invoice')
    invoice_items: Mapped[list['InvoiceItems']] = relationship('InvoiceItems', back_populates='invoice')
    validations: Mapped[list['Validations']] = relationship('Validations', back_populates='invoice')
    workflow_tasks: Mapped[list['WorkflowTasks']] = relationship('WorkflowTasks', back_populates='invoice')


class AuditLogs(Base):
    __tablename__ = 'audit_logs'
    __table_args__ = (
        CheckConstraint("actor_type::text = ANY (ARRAY['USER'::character varying, 'SYSTEM'::character varying]::text[])", name='audit_logs_actor_type_check'),
        ForeignKeyConstraint(['invoice_id'], ['invoices.id'], ondelete='CASCADE', name='fk_audit_logs_invoice'),
        PrimaryKeyConstraint('id', name='audit_logs_pkey'),
        Index('idx_audit_logs_created_at', 'created_at'),
        Index('idx_audit_logs_invoice', 'invoice_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    invoice_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    action: Mapped[str] = mapped_column(String(100), nullable=False)
    actor_type: Mapped[str] = mapped_column(String(20), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    actor_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    old_value: Mapped[Optional[str]] = mapped_column(Text)
    new_value: Mapped[Optional[str]] = mapped_column(Text)
    details: Mapped[Optional[str]] = mapped_column(Text)

    invoice: Mapped['Invoices'] = relationship('Invoices', back_populates='audit_logs')


class InvoiceItems(Base):
    __tablename__ = 'invoice_items'
    __table_args__ = (
        CheckConstraint('quantity > 0::numeric', name='invoice_items_quantity_check'),
        CheckConstraint('tax_rate >= 0::numeric AND tax_rate <= 100::numeric', name='invoice_items_tax_rate_check'),
        CheckConstraint('total_amount >= 0::numeric', name='invoice_items_total_amount_check'),
        CheckConstraint('unit_price >= 0::numeric', name='invoice_items_unit_price_check'),
        ForeignKeyConstraint(['invoice_id'], ['invoices.id'], ondelete='CASCADE', name='fk_invoice_items_invoice'),
        PrimaryKeyConstraint('id', name='invoice_items_pkey'),
        UniqueConstraint('invoice_id', 'line_number', name='unique_invoice_line'),
        Index('idx_invoice_items_invoice', 'invoice_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    invoice_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    line_number: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    quantity: Mapped[decimal.Decimal] = mapped_column(Numeric(15, 3), nullable=False)
    unit_price: Mapped[decimal.Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    tax_rate: Mapped[decimal.Decimal] = mapped_column(Numeric(5, 2), nullable=False, server_default=text('0'))
    total_amount: Mapped[decimal.Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    product_code: Mapped[Optional[str]] = mapped_column(String(100))

    invoice: Mapped['Invoices'] = relationship('Invoices', back_populates='invoice_items')


class Validations(Base):
    __tablename__ = 'validations'
    __table_args__ = (
        CheckConstraint("status::text = ANY (ARRAY['PASS'::character varying, 'FAIL'::character varying]::text[])", name='validations_status_check'),
        ForeignKeyConstraint(['invoice_id'], ['invoices.id'], ondelete='CASCADE', name='fk_validations_invoice'),
        PrimaryKeyConstraint('id', name='validations_pkey'),
        Index('idx_validations_invoice', 'invoice_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    invoice_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    validation_type: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    expected_value: Mapped[Optional[str]] = mapped_column(Text)
    actual_value: Mapped[Optional[str]] = mapped_column(Text)
    difference: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(15, 2))

    invoice: Mapped['Invoices'] = relationship('Invoices', back_populates='validations')


class WorkflowTasks(Base):
    __tablename__ = 'workflow_tasks'
    __table_args__ = (
        CheckConstraint("priority::text = ANY (ARRAY['LOW'::character varying, 'MEDIUM'::character varying, 'HIGH'::character varying, 'URGENT'::character varying]::text[])", name='workflow_tasks_priority_check'),
        CheckConstraint("status::text = ANY (ARRAY['PENDING'::character varying, 'IN_PROGRESS'::character varying, 'COMPLETED'::character varying, 'REJECTED'::character varying, 'CANCELLED'::character varying]::text[])", name='workflow_tasks_status_check'),
        ForeignKeyConstraint(['invoice_id'], ['invoices.id'], ondelete='CASCADE', name='fk_workflow_tasks_invoice'),
        PrimaryKeyConstraint('id', name='workflow_tasks_pkey'),
        Index('idx_workflow_tasks_invoice', 'invoice_id'),
        Index('idx_workflow_tasks_status', 'status')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    invoice_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    task_type: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False, server_default=text("'PENDING'::character varying"))
    priority: Mapped[str] = mapped_column(String(20), nullable=False, server_default=text("'MEDIUM'::character varying"))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    assigned_to: Mapped[Optional[int]] = mapped_column(BigInteger)
    reason: Mapped[Optional[str]] = mapped_column(Text)
    due_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    completed_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))

    invoice: Mapped['Invoices'] = relationship('Invoices', back_populates='workflow_tasks')
    approvals: Mapped[list['Approvals']] = relationship('Approvals', back_populates='task')


class Approvals(Base):
    __tablename__ = 'approvals'
    __table_args__ = (
        CheckConstraint("decision::text = ANY (ARRAY['APPROVED'::character varying, 'REJECTED'::character varying]::text[])", name='approvals_decision_check'),
        ForeignKeyConstraint(['task_id'], ['workflow_tasks.id'], ondelete='CASCADE', name='fk_approvals_task'),
        PrimaryKeyConstraint('id', name='approvals_pkey'),
        Index('idx_approvals_task', 'task_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    task_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    decision: Mapped[str] = mapped_column(String(20), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    approved_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    comment: Mapped[Optional[str]] = mapped_column(Text)

    task: Mapped['WorkflowTasks'] = relationship('WorkflowTasks', back_populates='approvals')


class Documents(Base):
    __tablename__ = "documents"

    __table_args__ = (
        CheckConstraint(
            "status::text = ANY (ARRAY["
            "'UPLOADED'::character varying, "
            "'OCR_PROCESSING'::character varying, "
            "'OCR_COMPLETED'::character varying, "
            "'EXTRACTION_PROCESSING'::character varying, "
            "'EXTRACTION_COMPLETED'::character varying, "
            "'FAILED'::character varying"
            "]::text[])",
            name="documents_status_check",
        ),
        PrimaryKeyConstraint("id", name="documents_pkey"),
        Index("idx_documents_status", "status"),
        Index("idx_documents_document_type", "document_type"),
    )

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    file_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    file_path: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    mime_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    file_size: Mapped[Optional[int]] = mapped_column(
        BigInteger,
    )

    document_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        server_default=text("'INVOICE'::character varying"),
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        server_default=text("'UPLOADED'::character varying"),
    )

    ocr_text: Mapped[Optional[str]] = mapped_column(
        Text,
    )

    extracted_data: Mapped[Optional[dict]] = mapped_column(
        JSONB,
    )

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )

    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )

