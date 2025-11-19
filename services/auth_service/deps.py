from typing import Union, Any
from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from utils import (
    ALGORITHM,
    JWT_SECRET_KEY
)

from jose import jwt
from pydantic import ValidationError
from schemas import TokenPayLoad, SystemUser

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