import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from jose import jwt

load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = 30
ALGORITHM = "HS256"

def create_access_token(data: dict):
    payload = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload.update({"exp": expire})
    access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return access_token

def decode_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

