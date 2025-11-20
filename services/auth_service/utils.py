from passlib.context import CryptContext
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from jose import jwt

load_dotenv()

# JWT constants
ACCESS_TOKEN_EXPIRE_MINUTES = 30
ALGORITHM = "HS256"
JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']   # can be string



# create context
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# generate a hashed password -> input: plain pass -> output: hashed pass
def get_hashed_password(password: str) -> str:
    return password_context.hash(password)

# verify a password
def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


# generate new JWT token and return
def create_access_token(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    # encode and generate JWT token
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode,JWT_SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt
