from uuid import UUID
from pydantic import BaseModel, Field
from typing import Optional

# Pydantic model schemas for types

class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str

class TokenPayLoad(BaseModel):
    sub: Optional[str] = None
    exp: Optional[int] = None

# TODO: update this based on user table mentioned in doc
class UserAuth(BaseModel):
    email: str = Field(..., description="user email")
    password: str = Field(..., min_length=5, max_length=24, description="user password")

class UserOut(BaseModel):
    id: UUID
    email: str

class SystemUser(UserOut):
    password: str
