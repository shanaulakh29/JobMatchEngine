from fastapi import Request, HTTPException
from jose import jwt, JWTError
from dotenv import load_dotenv
import os

load_dotenv() 

JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]
ALGORITHM = "HS256"

# paths that do NOT require auth
PUBLIC_PATHS = {
    "/login",
    "/auth/signup",
    "/health",
    "/"
}

async def authorize_middleware(request: Request, call_next):
    """Middleware for API Gateway.
    
    Purpose: Verifies incoming requests before they reach the consequent microservice
    
    """
    path = request.url.path

    # Skip auth for public routes
    if path=="/" or path.endswith(("/login", "/signup", "/health")):
        return await call_next(request)

    token = request.cookies.get("access_token")
    
    if not token:
        raise HTTPException(status_code=401, detail="Missing or invalid token")

    # verify token
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")

        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token payload")

        # attach user_id to request state
        request.state.user_id = user_id

    except JWTError:
        raise HTTPException(status_code=401, detail="Token verification failed")

    return await call_next(request)
