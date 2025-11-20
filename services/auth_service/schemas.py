from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID

# Pydantic model schemas for types and Service input/output

class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str

class TokenPayLoad(BaseModel):
    sub: Optional[str] = None
    exp: Optional[int] = None

# TODO: update this based on user table mentioned in doc
class UserAuth(BaseModel):
    username: str = Field(..., description="username")
    occupation: Optional[str] 
    email: str = Field(..., description="user email")
    password: str = Field(..., min_length=5, max_length=24, description="user password")

class UserOut(BaseModel):
    id: int
    username: str
    email: str
    occupation: str
    created_at: datetime
  
