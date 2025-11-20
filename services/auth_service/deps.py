from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from auth_service.utils import (
    ALGORITHM,
    JWT_SECRET_KEY
)
from auth_service.db import db_query, db_execute
from jose import jwt, JWTError
from pydantic import ValidationError


from auth_service.schemas import TokenPayLoad, UserOut

# defining get current user as dependency
reusable_oauth = OAuth2PasswordBearer (
    tokenUrl= "/auth/login",
    scheme_name="JWT"
)

# function to validate the current user
async def get_current_user(token: str = Depends(reusable_oauth)) -> UserOut:
    try:
        payload = jwt.decode(
            token, JWT_SECRET_KEY, algorithms=[ALGORITHM]
        ) 
        token_data = TokenPayLoad(**payload)
        
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code= status.HTTP_401_UNAUTHORIZED,
                detail= "Token expired. Please refresh",
                headers={"WWW-Authenticate": "Bearer"},
            )
    # catch any errors
    except(JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # get the user
    user = db_query("SELECT id, username, email, occupation, created_at FROM users u WHERE u.email = %s", (token_data.sub,))
   

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
    )
    return UserOut(id=user[0][0], username=user[0][1], email=user[0][2], occupation=user[0][3], created_at=user[0][4])