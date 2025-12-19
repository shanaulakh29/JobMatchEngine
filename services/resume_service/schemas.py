from pydantic import BaseModel, Field
from datetime import datetime

# pydantic model schemas for types and service input/output

class Resume(BaseModel):
    s3_key: str
    status: str
    uploaded_at: datetime
    
