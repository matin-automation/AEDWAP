BEGIN;
INSERT INTO vendors
(name, gst_number, email, phone, address, status)
VALUES

('Tata Industrial Supplies Pvt Ltd',
 '27AABCT1234F1Z5',
 'accounts@tataindustrial.example',
 '9876543210',
 'Pune, Maharashtra',
 'ACTIVE'),

('Mahindra Components Ltd',
 '27AABCM5678G1Z2',
 'finance@mahindracomponents.example',
 '9876543211',
 'Mumbai, Maharashtra',
 'ACTIVE'),

('Pune Office Solutions',
 '27AABCP9012H1Z8',
 'billing@puneofficesolutions.example',
 '9876543212',
 'Pune, Maharashtra',
 'ACTIVE'),

('TechNova Systems Pvt Ltd',
 '29AABCT3456J1Z6',
 'accounts@technova.example',
 '9876543213',
 'Bengaluru, Karnataka',
 'ACTIVE'),

('Global Packaging Industries',
 '27AABCG7890K1Z4',
 'invoices@globalpackaging.example',
 '9876543214',
 'Nashik, Maharashtra',
 'ACTIVE');



INSERT INTO purchase_orders
(po_number, vendor_id, po_date, currency,
 subtotal, tax_amount, total_amount, status)
VALUES

(
 'PO-2026-0001',
 (SELECT id FROM vendors WHERE gst_number = '27AABCT1234F1Z5'),
 '2026-07-01',
 'INR',
 100000.00,
 18000.00,
 118000.00,
 'OPEN'
),

(
 'PO-2026-0002',
 (SELECT id FROM vendors WHERE gst_number = '27AABCM5678G1Z2'),
 '2026-07-03',
 'INR',
 75000.00,
 13500.00,
 88500.00,
 'OPEN'
),

(
 'PO-2026-0003',
 (SELECT id FROM vendors WHERE gst_number = '27AABCP9012H1Z8'),
 '2026-07-05',
 'INR',
 50000.00,
 9000.00,
 59000.00,
 'OPEN'
),

(
 'PO-2026-0004',
 (SELECT id FROM vendors WHERE gst_number = '29AABCT3456J1Z6'),
 '2026-07-08',
 'INR',
 120000.00,
 21600.00,
 141600.00,
 'OPEN'
),

(
 'PO-2026-0005',
 (SELECT id FROM vendors WHERE gst_number = '27AABCG7890K1Z4'),
 '2026-07-10',
 'INR',
 80000.00,
 14400.00,
 94400.00,
 'OPEN'
);




-- Invoice 1
-- PERFECT MATCH WITH PO

INSERT INTO invoices
(invoice_number, vendor_id, purchase_order_id,
 invoice_date, due_date, currency,
 subtotal, tax_amount, total_amount, status)
VALUES
(
 'INV-TATA-001',
 (SELECT id FROM vendors WHERE gst_number = '27AABCT1234F1Z5'),
 (SELECT id FROM purchase_orders WHERE po_number = 'PO-2026-0001'),
 '2026-07-15',
 '2026-08-14',
 'INR',
 100000.00,
 18000.00,
 118000.00,
 'APPROVED'
);


-- Invoice 2
-- PERFECT MATCH WITH PO

INSERT INTO invoices
(invoice_number, vendor_id, purchase_order_id,
 invoice_date, due_date, currency,
 subtotal, tax_amount, total_amount, status)
VALUES
(
 'INV-MAH-001',
 (SELECT id FROM vendors WHERE gst_number = '27AABCM5678G1Z2'),
 (SELECT id FROM purchase_orders WHERE po_number = 'PO-2026-0002'),
 '2026-07-18',
 '2026-08-17',
 'INR',
 75000.00,
 13500.00,
 88500.00,
 'PROCESSED'
);


-- Invoice 3
-- AMOUNT MISMATCH WITH PO
-- PO = 59,000
-- Invoice = 62,000

INSERT INTO invoices
(invoice_number, vendor_id, purchase_order_id,
 invoice_date, due_date, currency,
 subtotal, tax_amount, total_amount, status)
VALUES
(
 'INV-POS-001',
 (SELECT id FROM vendors WHERE gst_number = '27AABCP9012H1Z8'),
 (SELECT id FROM purchase_orders WHERE po_number = 'PO-2026-0003'),
 '2026-07-20',
 '2026-08-19',
 'INR',
 52542.37,
 9457.63,
 62000.00,
 'REVIEW_REQUIRED'
);


-- Invoice 4
-- PERFECT MATCH

INSERT INTO invoices
(invoice_number, vendor_id, purchase_order_id,
 invoice_date, due_date, currency,
 subtotal, tax_amount, total_amount, status)
VALUES
(
 'INV-TECH-001',
 (SELECT id FROM vendors WHERE gst_number = '29AABCT3456J1Z6'),
 (SELECT id FROM purchase_orders WHERE po_number = 'PO-2026-0004'),
 '2026-07-22',
 '2026-08-21',
 'INR',
 120000.00,
 21600.00,
 141600.00,
 'PENDING_APPROVAL'
);


-- Invoice 5
-- TAX MISMATCH / VALIDATION FAILURE

INSERT INTO invoices
(invoice_number, vendor_id, purchase_order_id,
 invoice_date, due_date, currency,
 subtotal, tax_amount, total_amount, status)
VALUES
(
 'INV-GPI-001',
 (SELECT id FROM vendors WHERE gst_number = '27AABCG7890K1Z4'),
 (SELECT id FROM purchase_orders WHERE po_number = 'PO-2026-0005'),
 '2026-07-25',
 '2026-08-24',
 'INR',
 80000.00,
 12000.00,
 92000.00,
 'REVIEW_REQUIRED'
);


-- Invoice 6
-- NO PURCHASE ORDER
-- Useful for exception handling

INSERT INTO invoices
(invoice_number, vendor_id, purchase_order_id,
 invoice_date, due_date, currency,
 subtotal, tax_amount, total_amount, status)
VALUES
(
 'INV-TATA-002',
 (SELECT id FROM vendors WHERE gst_number = '27AABCT1234F1Z5'),
 NULL,
 '2026-07-28',
 '2026-08-27',
 'INR',
 45000.00,
 8100.00,
 53100.00,
 'RECEIVED'
);




INSERT INTO invoice_items
(invoice_id, line_number, description,
 product_code, quantity, unit_price, tax_rate, total_amount)
VALUES

(
 (SELECT id FROM invoices WHERE invoice_number = 'INV-TATA-001'),
 1,
 'Industrial Bearings',
 'BRG-100',
 100,
 500.00,
 18.00,
 50000.00
),

(
 (SELECT id FROM invoices WHERE invoice_number = 'INV-TATA-001'),
 2,
 'Steel Fasteners',
 'STF-200',
 500,
 60.00,
 18.00,
 30000.00
),

(
 (SELECT id FROM invoices WHERE invoice_number = 'INV-TATA-001'),
 3,
 'Machine Lubricant',
 'LUB-300',
 100,
 200.00,
 18.00,
 20000.00
);



INSERT INTO invoice_items
(invoice_id, line_number, description,
 product_code, quantity, unit_price, tax_rate, total_amount)
VALUES

(
 (SELECT id FROM invoices WHERE invoice_number = 'INV-MAH-001'),
 1,
 'Automotive Components',
 'AUTO-101',
 50,
 1000.00,
 18.00,
 50000.00
),

(
 (SELECT id FROM invoices WHERE invoice_number = 'INV-MAH-001'),
 2,
 'Engine Mounting Brackets',
 'AUTO-202',
 100,
 250.00,
 18.00,
 25000.00
);




INSERT INTO invoice_items
(invoice_id, line_number, description,
 product_code, quantity, unit_price, tax_rate, total_amount)
VALUES

(
 (SELECT id FROM invoices WHERE invoice_number = 'INV-POS-001'),
 1,
 'Office Desks',
 'DESK-100',
 20,
 1500.00,
 18.00,
 30000.00
),

(
 (SELECT id FROM invoices WHERE invoice_number = 'INV-POS-001'),
 2,
 'Ergonomic Office Chairs',
 'CHAIR-200',
 15,
 1200.00,
 18.00,
 18000.00
),

(
 (SELECT id FROM invoices WHERE invoice_number = 'INV-POS-001'),
 3,
 'Office Accessories',
 'ACC-300',
 1,
 4542.37,
 18.00,
 4542.37
);




INSERT INTO invoice_items
(invoice_id, line_number, description,
 product_code, quantity, unit_price, tax_rate, total_amount)
VALUES

(
 (SELECT id FROM invoices WHERE invoice_number = 'INV-TECH-001'),
 1,
 'Enterprise Servers',
 'SRV-100',
 4,
 25000.00,
 18.00,
 100000.00
),

(
 (SELECT id FROM invoices WHERE invoice_number = 'INV-TECH-001'),
 2,
 'Network Switches',
 'NET-200',
 4,
 5000.00,
 18.00,
 20000.00
);




INSERT INTO invoice_items
(invoice_id, line_number, description,
 product_code, quantity, unit_price, tax_rate, total_amount)
VALUES

(
 (SELECT id FROM invoices WHERE invoice_number = 'INV-GPI-001'),
 1,
 'Corrugated Packaging Boxes',
 'BOX-100',
 1000,
 50.00,
 15.00,
 50000.00
),

(
 (SELECT id FROM invoices WHERE invoice_number = 'INV-GPI-001'),
 2,
 'Protective Packaging Material',
 'PKG-200',
 600,
 50.00,
 15.00,
 30000.00
);




INSERT INTO invoice_items
(invoice_id, line_number, description,
 product_code, quantity, unit_price, tax_rate, total_amount)
VALUES

(
 (SELECT id FROM invoices WHERE invoice_number = 'INV-TATA-002'),
 1,
 'Replacement Machine Parts',
 'REP-100',
 30,
 1000.00,
 18.00,
 30000.00
),

(
 (SELECT id FROM invoices WHERE invoice_number = 'INV-TATA-002'),
 2,
 'Maintenance Materials',
 'REP-200',
 15,
 1000.00,
 18.00,
 15000.00
);




INSERT INTO validations
(invoice_id, validation_type, status,
 expected_value, actual_value, difference, message)
VALUES

(
 (SELECT id FROM invoices WHERE invoice_number = 'INV-TATA-001'),
 'PO_AMOUNT_MATCH',
 'PASS',
 '118000.00',
 '118000.00',
 0,
 'Invoice total matches purchase order total.'
),

(
 (SELECT id FROM invoices WHERE invoice_number = 'INV-TATA-001'),
 'SUBTOTAL_CALCULATION',
 'PASS',
 '100000.00',
 '100000.00',
 0,
 'Invoice subtotal matches sum of invoice items.'
),

(
 (SELECT id FROM invoices WHERE invoice_number = 'INV-TATA-001'),
 'TAX_CALCULATION',
 'PASS',
 '18000.00',
 '18000.00',
 0,
 'Invoice tax amount is correct.'
);




INSERT INTO validations
(invoice_id, validation_type, status,
 expected_value, actual_value, difference, message)
VALUES

(
 (SELECT id FROM invoices WHERE invoice_number = 'INV-MAH-001'),
 'PO_AMOUNT_MATCH',
 'PASS',
 '88500.00',
 '88500.00',
 0,
 'Invoice total matches purchase order total.'
),

(
 (SELECT id FROM invoices WHERE invoice_number = 'INV-MAH-001'),
 'SUBTOTAL_CALCULATION',
 'PASS',
 '75000.00',
 '75000.00',
 0,
 'Invoice subtotal matches invoice items.'
);



INSERT INTO validations
(invoice_id, validation_type, status,
 expected_value, actual_value, difference, message)
VALUES

(
 (SELECT id FROM invoices WHERE invoice_number = 'INV-POS-001'),
 'PO_AMOUNT_MATCH',
 'FAIL',
 '59000.00',
 '62000.00',
 3000.00,
 'Invoice total exceeds purchase order total by INR 3,000.'
),

(
 (SELECT id FROM invoices WHERE invoice_number = 'INV-POS-001'),
 'SUBTOTAL_CALCULATION',
 'PASS',
 '52542.37',
 '52542.37',
 0,
 'Invoice subtotal matches invoice items.'
);



INSERT INTO validations
(invoice_id, validation_type, status,
 expected_value, actual_value, difference, message)
VALUES

(
 (SELECT id FROM invoices WHERE invoice_number = 'INV-TECH-001'),
 'PO_AMOUNT_MATCH',
 'PASS',
 '141600.00',
 '141600.00',
 0,
 'Invoice total matches purchase order total.'
),

(
 (SELECT id FROM invoices WHERE invoice_number = 'INV-TECH-001'),
 'SUBTOTAL_CALCULATION',
 'PASS',
 '120000.00',
 '120000.00',
 0,
 'Invoice subtotal matches invoice items.'
);



INSERT INTO validations
(invoice_id, validation_type, status,
 expected_value, actual_value, difference, message)
VALUES

(
 (SELECT id FROM invoices WHERE invoice_number = 'INV-GPI-001'),
 'PO_AMOUNT_MATCH',
 'FAIL',
 '94400.00',
 '92000.00',
 -2400.00,
 'Invoice total differs from purchase order total by INR 2,400.'
),

(
 (SELECT id FROM invoices WHERE invoice_number = 'INV-GPI-001'),
 'TAX_RATE_CHECK',
 'FAIL',
 '18.00%',
 '15.00%',
 -3.00,
 'Invoice uses a 15% tax rate while expected tax rate is 18%.'
);




INSERT INTO validations
(invoice_id, validation_type, status,
 expected_value, actual_value, difference, message)
VALUES

(
 (SELECT id FROM invoices WHERE invoice_number = 'INV-TATA-002'),
 'PO_EXISTENCE',
 'FAIL',
 'Purchase Order Required',
 'No Purchase Order',
 NULL,
 'Invoice does not reference a purchase order and requires manual review.'
);


INSERT INTO workflow_tasks
(invoice_id, task_type, status, priority, reason, due_at)
VALUES

(
 (SELECT id FROM invoices WHERE invoice_number = 'INV-POS-001'),
 'AMOUNT_MISMATCH_REVIEW',
 'PENDING',
 'HIGH',
 'Invoice total exceeds purchase order total.',
 '2026-08-21 17:00:00+05:30'
),

(
 (SELECT id FROM invoices WHERE invoice_number = 'INV-GPI-001'),
 'TAX_VALIDATION_REVIEW',
 'PENDING',
 'HIGH',
 'Tax rate and invoice total do not match expected purchase order values.',
 '2026-08-22 17:00:00+05:30'
),

(
 (SELECT id FROM invoices WHERE invoice_number = 'INV-TATA-002'),
 'MISSING_PO_REVIEW',
 'PENDING',
 'URGENT',
 'Invoice received without a purchase order.',
 '2026-08-21 12:00:00+05:30'
),

(
 (SELECT id FROM invoices WHERE invoice_number = 'INV-TECH-001'),
 'MANAGER_APPROVAL',
 'COMPLETED',
 'MEDIUM',
 'Invoice passed automated validation and requires approval.',
 '2026-08-20 17:00:00+05:30'
);



INSERT INTO approvals
(task_id, decision, approved_by, comment)
VALUES

(
 (
   SELECT id
   FROM workflow_tasks
   WHERE invoice_id = (
       SELECT id
       FROM invoices
       WHERE invoice_number = 'INV-TECH-001'
   )
   AND task_type = 'MANAGER_APPROVAL'
 ),
 'APPROVED',
 1001,
 'Invoice validated successfully and approved for processing.'
);



INSERT INTO audit_logs
(invoice_id, action, actor_type, actor_id,
 old_value, new_value, details)
VALUES

(
 (SELECT id FROM invoices WHERE invoice_number = 'INV-TATA-001'),
 'INVOICE_RECEIVED',
 'SYSTEM',
 NULL,
 NULL,
 'RECEIVED',
 'Invoice successfully received by the automation platform.'
),

(
 (SELECT id FROM invoices WHERE invoice_number = 'INV-TATA-001'),
 'VALIDATION_COMPLETED',
 'SYSTEM',
 NULL,
 'VALIDATING',
 'APPROVED',
 'All automated validation checks passed.'
),

(
 (SELECT id FROM invoices WHERE invoice_number = 'INV-POS-001'),
 'VALIDATION_FAILED',
 'SYSTEM',
 NULL,
 'VALIDATING',
 'REVIEW_REQUIRED',
 'Purchase order amount mismatch detected.'
),

(
 (SELECT id FROM invoices WHERE invoice_number = 'INV-GPI-001'),
 'VALIDATION_FAILED',
 'SYSTEM',
 NULL,
 'VALIDATING',
 'REVIEW_REQUIRED',
 'Tax validation failed.'
),

(
 (SELECT id FROM invoices WHERE invoice_number = 'INV-TECH-001'),
 'APPROVED',
 'USER',
 1001,
 'PENDING_APPROVAL',
 'APPROVED',
 'Manager approved invoice for processing.'
),

(
 (SELECT id FROM invoices WHERE invoice_number = 'INV-TATA-002'),
 'REVIEW_REQUIRED',
 'SYSTEM',
 NULL,
 'RECEIVED',
 'REVIEW_REQUIRED',
 'Invoice has no associated purchase order.'
);

COMMIT;

