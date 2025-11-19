from deps import get_current_user
from db import init_db, db_execute, db_query
from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from schemas import UserOut, UserAuth, TokenSchema
from utils import (
    get_hashed_password,
    create_access_token,
    create_refresh_token,
    verify_password
)


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
    # get user from database -> checks the user email
    user = db_query("SELECT username, password_hash FROM users u WHERE u.email = %s", (form_data.username,))
    
    # wrong email/password
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    hashed_pass = user[0]['password_hash']
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    return {
        "access_token": create_access_token(user['email']),
        "refresh_token": create_refresh_token(user['email'])
    }
    

# user signup
@app.post('/auth/signup', summary="Create new user", response_model=UserOut)
async def create_user(data: UserAuth):
    
    # query database to check if the user already exists
    user = db_query("SELECT email FROM users u WHERE u.email = %s", (data.username,))
    
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    params = (
        data.email,
        get_hashed_password(data.password),
        data.username,
        data.occupation
    )
    
  
    # Store the user in database
    db_execute("INSERT INTO users (email, password, username, occupation) VALUES (%s, %s, %s, %s)", params)
    
    # query for created user
    response = db_query("SELECT * FROM users WHERE username = %s", (params[2],))
    
    json_filtered = {
        "id": response[0]['id'],
        "username": response[0]['username'],
        "email": response[0]['email'],
        "occupation": response[0]['occupation']
    }
    
    return JSONResponse(
        content= json_filtered,
        status_code=201
    )

# validate user
@app.get('/auth/validate', summary='Get details of currently logged in user', response_model=UserOut)
async def get_user(user: UserOut = Depends(get_current_user)):
    return user

# call init_db function (generate tables) on startup
if __name__ == "__main__":
    init_db()