from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class DocumentCreate(BaseModel):
    file_name: str
    mime_type: str
    file_size: Optional[int] = None
    document_type: str = "INVOICE"


class DocumentResponse(BaseModel):
    id: int
    file_name: str
    file_path: str
    mime_type: str
    file_size: Optional[int]
    document_type: str
    status: str
    ocr_text: Optional[str]
    extracted_data: Optional[dict]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

