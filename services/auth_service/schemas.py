from pydantic import BaseModel, Field
from typing import Optional

# Pydantic model schemas for types and Service input/output

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    exp: Optional[int] = None


# schema of user withotu password, to be returned
class User(BaseModel):
    id: int
    username: str = Field(..., description="username")
    occupation: Optional[str] 
    email: str = Field(..., description="user email")
    
# user in database, including hashed password 
class UserInDB(User):
    password_hash: str
  
    
#  used when user is signing up first time
class UserAuth(BaseModel):
    id: int
    username: str = Field(..., description="username")
    password: str = Field(..., description="user password")
    occupation: Optional[str] 
    email: str = Field(..., description="user email")
    
class UserSignup(BaseModel):
    username: str
    password: str
    email: str
    occupation: Optional[str] = None
