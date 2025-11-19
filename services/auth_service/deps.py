from typing import Union, Any
from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from utils import (
    ALGORITHM,
    JWT_SECRET_KEY
)

from jose import jwt, JWTError
from pydantic import ValidationError

# TODO
from schemas import TokenPayLoad, SystemUser

# defining get current user as dependency
reusable_oauth = OAuth2PasswordBearer (
    tokenUrl= "/auth/login",
    scheme_name="JWT"
)

# function to validate the current user
async def get_current_user(token: str = Depends(reusable_oauth)) -> SystemUser:
    try:
        payload = jwt.decode(
            token, JWT_SECRET_KEY, algorithms=[ALGORITHM]
        )
        token_data = TokenPayLoad(**payload)
        
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code= status.HTTP_401_UNAUTHORIZED,
                detail= "Token expired",
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
    # TODO
    user: Union[dict[str, Any], None] = db.get(token_data.sub, None)
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
    )
    return SystemUser(**user)