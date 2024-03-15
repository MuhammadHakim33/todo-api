from datetime import datetime, timedelta, timezone
from jose import jwt

SECRET_KEY = 'd2lsZGJldHRlcmJyaWdodGV4Y2xhaW1lZGdvb3Nlc2E'
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

