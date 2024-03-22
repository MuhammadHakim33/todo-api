from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from models.model_user import RegisterModel, LoginModel, LoginModel, UserBase
from service.service_token import decode_token
from repository.repository_user import UserRepository
from passlib.context import CryptContext
from jose import JWTError

pwd_context = CryptContext(schemes=["sha256_crypt"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/login")
repo_user = UserRepository()

def verified_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_token(token)
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = repo_user.find({'email': email})
    if user is None:
        raise credentials_exception
    return UserBase(**user)

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def email_must_unique(email):
    result = repo_user.find({'email': email})
    if result:
        raise HTTPException(detail='Email is already registered', status_code=409)
    return True

def create_user(user: RegisterModel):
    email_must_unique(user.email)

    hash = get_password_hash(user.password)
    user.password = hash
    result = repo_user.create(user)
    return result

def auth(form_data: LoginModel):
    user_logged = repo_user.find({'email': form_data.email})
    if not user_logged:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    user = LoginModel(**user_logged)
    hashed_password = verify_password(form_data.password, user.password)
    if not hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    return user