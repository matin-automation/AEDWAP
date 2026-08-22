from pydantic import BaseModel, ConfigDict
import datetime

class VendorOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    status: str
    gst_number: str | None
    email: str | None
    phone: str | None
    address: str | None
    created_at: datetime.datetime
    updated_at: datetime.datetime