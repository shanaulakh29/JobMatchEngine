from fastapi import FastAPI, status, HTTPException
from fastapi.responses import RedirectResponse
from schemas import UserOut, UserAuth               # TODO
from utils import get_hashed_password
from uuid import uuid4

app = FastAPI()

# status check
@app.get("/auth/status", summary="Status check")
async def root():
    return {"description": "Auth service for JobMatchEngine", 
            "status": "Running OK"
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