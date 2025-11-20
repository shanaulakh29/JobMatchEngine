from auth_service.deps import get_current_user
from auth_service.db import init_db, db_execute, db_query
from auth_service.schemas import UserOut, UserAuth, TokenSchema
from auth_service.utils import (
    get_hashed_password,
    create_access_token,
    create_refresh_token,
    verify_password
)
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse


# on startup build tables
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db();
    yield

app = FastAPI(lifespan=lifespan)




# status check
@app.get('/', summary="Status check")
async def root():
    return {"description": "Auth service for JobMatchEngine", 
            "status": "Running OK"
            }

# user login
# function uses OAuth2PasswordRequestForm as a dependency
@app.post('/login', summary="Create access and refresh tokens for user", response_model=TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # get user from database -> checks the user email
    user = db_query("SELECT email, password_hash FROM users u WHERE u.email = %s", (form_data.username,))
    # wrong email/password
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
        
   
    hashed_pass = user[0][1]
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    return {
        "access_token": create_access_token(user[0][0]),
        "refresh_token": create_refresh_token(user[0][0])
    }
    

# user signup
@app.post('/signup', summary="Create new user", response_model=UserOut)
async def create_user(data: UserAuth):
    
    # query database to check if the user already exists
    user = db_query("SELECT email FROM users u WHERE u.email = %s", (data.email,))
 
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    dt = datetime.now(timezone.utc)
    params = (
        data.email,
        get_hashed_password(data.password),
        data.username,
        data.occupation,
        dt 
    )
    
    # Store the user in database
    db_execute("INSERT INTO users (email, password_hash, username, occupation, created_at) VALUES (%s, %s, %s, %s, %s)", params)
    

    return JSONResponse(
        content= "User created successfully.",
        status_code=201
    )
    
    
# @app.post('/auth/refresh', summary="Refresh the access token if expired", response_model=TokenSchema)
# async def refresh_token(data:)
    

# validate user
@app.get('/auth/validate', summary='Get details of currently logged in user', response_model=UserOut)
async def get_user(user: UserOut = Depends(get_current_user)):
    return user

