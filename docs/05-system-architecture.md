                       VENDOR
                         │
                         │ Invoice
                         ▼
              ┌────────────────────┐
              │   DOCUMENT INTAKE  │
              │                    │
              │ Upload / Email     │
              └─────────┬──────────┘
                        ↓
              ┌────────────────────┐
              │ Document AI / OCR  │
              └─────────┬──────────┘
                        ↓
              ┌────────────────────┐
              │ LLM Extraction     │
              └─────────┬──────────┘
                        ↓
              ┌────────────────────┐
              │ Validation Engine  │
              └─────────┬──────────┘
                        │
            ┌───────────┼───────────┐
            ↓           ↓           ↓
          Vendor        PO        Duplicate
          Check        Match       Check
            │           │           │
            └───────────┼───────────┘
                        ↓
                 RAG Policy Check
                        ↓
                Workflow / Agent
                   /         \
                  ↓           ↓
             Auto Process   Human Review
                  │           │
                  └─────┬─────┘
                        ↓
                 ERP Simulation
                        ↓
                   PostgreSQL
                        ↓
                   Audit Logs
