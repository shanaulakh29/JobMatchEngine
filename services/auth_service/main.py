from auth_service.deps import get_current_user
from auth_service.db import init_db, db_execute, db_query
from auth_service.schemas import User, Token, UserSignup
from auth_service.utils import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    get_hashed_password,
    create_access_token,
        ALGORITHM,
    JWT_SECRET_KEY,
    verify_password
)

from auth_service.deps import get_current_user, authenticate_user
from contextlib import asynccontextmanager
from datetime import datetime, timezone, timedelta
from fastapi import FastAPI, status, HTTPException, Depends, Response, Form, Cookie
from fastapi.responses import JSONResponse
from typing import Optional
from jose import jwt, JWTError
from auth_service.schemas import TokenData
from auth_service.deps import get_user



@asynccontextmanager
async def lifespan(app: FastAPI):
    """Builds tables on application startup"""
    init_db()
    yield

app = FastAPI(lifespan=lifespan, title="Auth Service")



# status check
@app.get('/health', summary="Status check")
async def root():
    return {"description": "Auth service for JobMatchEngine", 
            "status": "Running OK"
            }
    

# user login
@app.post('/login', summary="Create login access for user and return access token")
async def login(response: Response = None, username: str = Form(...), password: str = Form(...)):

    # authenticate the user
    user = authenticate_user(username, password) # type: ignore
    
    
    # raise exception if no user 
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # expiration time
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # create a access token for the user
    access_token = create_access_token(data={"sub": user.username,
                                             "user_id": user.id}, expires_delta=access_token_expires)
    
    
    response = JSONResponse(content={"messsage": "Logged in successfully"})

    # set the cookie
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True, # prevent JS access (security),
        secure=False, # TODO: Set this to true for production
        max_age=3600, # Expiration in seconds
        domain=None,
        samesite="lax",
        path="/"
    )
    return response
    
    
# user signup
@app.post('/signup', summary="Create new user")
async def create_user(username: str = Form(...), password: str = Form(...), email: str = Form(...), occupation: str | None = Form(None)):
    
    
    # query database to check if the user already exists
    user = db_query("SELECT email FROM users u WHERE u.email = %s", (email,))
 
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )

    dt = datetime.now(timezone.utc)
    params = (
        email,
        get_hashed_password(password),
        username,
        occupation,
        dt 
    )
    
    # Store the user in database
    db_execute("INSERT INTO users (email, password_hash, username, occupation, created_at) VALUES (%s, %s, %s, %s, %s)", params)
    
    
    return JSONResponse(
        content= "User created successfully.",
        status_code=201
    )

@app.post("/logout")
def logout():
    response = JSONResponse(content={"messsage": "Logged out successfully"})
    response.delete_cookie(
        key="access_token",
        httponly=True,
        samesite="lax",
        secure=False, #true in production
        path="/",
        domain=None,
    )
    return response

@app.post("/validate-token")
def validateToken(access_token: Optional[str] = Cookie(None)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    try:
        payload = jwt.decode(access_token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credential_exception
        
        token_data = TokenData(username=username)
    except JWTError:
        raise credential_exception
    
    user = get_user(username=token_data.username) # type: ignore
    #  check if user exists in database
    if user is None:
        raise credential_exception

    return JSONResponse(content={"message": "Token is valid", "user": {"id": user.id, "username": user.username, "email": user.email}})


# validate user
@app.get('/validate', summary='Get details of currently logged in user', response_model=User)
async def read_user(current_user: User = Depends(get_current_user)):
   return current_user

