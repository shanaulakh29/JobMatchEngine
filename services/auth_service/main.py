from auth_service.deps import get_current_user
from auth_service.db import init_db, db_execute, db_query
from auth_service.schemas import User, Token, UserSignup
from auth_service.utils import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    get_hashed_password,
    create_access_token,
)
from auth_service.deps import get_current_user, authenticate_user
from contextlib import asynccontextmanager
from datetime import datetime, timezone, timedelta
from fastapi import FastAPI, status, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from auth_service.middlewares.login_middleware import login_middleware



@asynccontextmanager
async def lifespan(app: FastAPI):
    """Builds tables on application startup"""
    init_db()
    yield

app = FastAPI(lifespan=lifespan, title="Auth Service")
app.middleware("http")(login_middleware)


# status check
@app.get('/health', summary="Status check")
async def root():
    return {"description": "Auth service for JobMatchEngine", 
            "status": "Running OK"
            }

# user login
# function uses OAuth2PasswordRequestForm as a dependency
# OAuth2PasswordRequestForm -> specifies that the data will be in form of username and password.
@app.post('/login', summary="Create login access for user and return access token", response_model=Token)
async def login(request: Request):
    form_data = getattr(request.state, "form_data", {})
    # authenticate the user
    username = form_data.get("username")
    password = form_data.get("password")
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
    
    # return the generated token
    return {"access_token": access_token, "token_type": "bearer"}
    

    

# user signup
@app.post('/signup', summary="Create new user")
async def create_user(data: UserSignup):
    
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

    
# validate user
@app.get('/validate', summary='Get details of currently logged in user', response_model=User)
async def read_user(current_user: User = Depends(get_current_user)):
   return current_user

