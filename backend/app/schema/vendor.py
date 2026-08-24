from pydantic import BaseModel, EmailStr
from typing import Optional


class VendorCreate(BaseModel):
    name: str
    gst_number: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None


class VendorResponse(BaseModel):
    id: int
    name: str
    status: str
    gst_number: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None

    model_config = {
        "from_attributes": True
    }