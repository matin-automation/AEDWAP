from app.core.database import SessionLocal
from app.models.models import Vendors

db = SessionLocal()

try:
    vendors = db.query(Vendors).all()

    print(f"Found {len(vendors)} vendors")

    for vendor in vendors:
        print(vendor.id, vendor.name, vendor.gst_number)

finally:
    db.close()