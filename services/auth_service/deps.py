from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from auth_service.utils import (
    ALGORITHM,
    JWT_SECRET_KEY,
    verify_password
    
)
from auth_service.db import db_query
from jose import jwt, JWTError
from auth_service.schemas import TokenData, UserInDB

# defining get current user as dependency
oauth2_scheme = OAuth2PasswordBearer (
    tokenUrl= "/login",
    scheme_name="JWT"
)

# function to get a user
def get_user(username: str) -> UserInDB:
    # get the user
    user = db_query("SELECT id, username, email, occupation, password_hash FROM users u WHERE u.username = %s", (username,))

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
    )
        
    return UserInDB(id=user[0][0], username=user[0][1], email=user[0][2], occupation=user[0][3], password_hash=user[0][4])

# function to authenticate user
def authenticate_user(username: str, password: str) -> UserInDB:
    user: UserInDB = get_user(username)
    
    # make sure exists and password is correct
    if not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incorrect password",
        )
    
    return user

# function to get curent user
async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserInDB:
    
    # credential exception. To be used throughout function to raise exception
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    
    try:
        # decode the token
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        
        # get the username encoded in token
        username = payload.get("sub")
        
        # check if username exists
        if username is None:
            raise credential_exception
        
        token_data = TokenData(username=username)
        
    
    except JWTError:
        raise credential_exception
    
    user = get_user(username=token_data.username) # type: ignore
    #  check if user exists in database
    if user is None:
        raise credential_exception

    return user
    


    
    