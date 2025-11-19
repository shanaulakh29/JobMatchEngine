from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from schemas import UserOut, UserAuth, TokenSchema               # TODO
from utils import (
    get_hashed_password,
    create_access_token,
    create_refresh_token,
    verify_password
)
from uuid import uuid4

app = FastAPI()

# status check
@app.get('/auth/status', summary="Status check")
async def root():
    return {"description": "Auth service for JobMatchEngine", 
            "status": "Running OK"
            }

# user login
# function uses OAuth2PasswordRequestForm as a dependency
@app.post('/auth/login', summary="Create access and refresh tokens for user", response_model=TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # get user from database
    # TODO
    # user = db.get(form_data.username, None)
    user = True
    
    # wrong email/password
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    hashed_pass = user['password']
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST
            detail="Incorrect email or password"
        )
    return {
        "access_token": create_access_token(user['email']),
        "refresh_token": create_refresh_token(user['email'])
    }
    

# user signup
@app.post('/auth/signup', summary="Create new user", response_model=UserOut)
async def create_user(data: UserAuth):
    
    # TODO
    # query database to check if the user already exists
    user = True
    
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    user = {
        'email': data.email,
        "password": get_hashed_password(data.password),
        'id': str(uuid4())
    }
    
    # TODO
    # Store the user in database
    return user