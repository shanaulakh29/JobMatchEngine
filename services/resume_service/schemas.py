from pydantic import BaseModel, Field
from typing import Optional

# pydantic model schemas for types and service input/output

class Resume(BaseModel):
    s3_key: str
    status: str
    uploaded_at: str
    
