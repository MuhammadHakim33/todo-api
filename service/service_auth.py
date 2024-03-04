from fastapi import Depends, HTTPException
from models.model_user import RegisterModel, LoginModel, UserBase
from service.service_token import TokenJWT
from repository.repository_user import UserRepository
from passlib.context import CryptContext

class AuthService:
    def __init__(self, repo_user: UserRepository = Depends()):
        self.pwd_context = CryptContext(schemes=["sha256_crypt"])
        self.repo_user = repo_user

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)
    
    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def email_must_unique(self, email):
        result = self.repo_user.find({'email': email})
        if result:
            raise HTTPException(detail='Email is already registered', status_code=409)
        return True

    def register(self, user: RegisterModel):
        self.email_must_unique(user.email)

        hash = self.get_password_hash(user.password)
        user.password = hash
        return self.repo_user.create(user)
    
    def auth(self, form_data: LoginModel):
        user_logged = self.repo_user.find({'email': form_data.email})
        if not user_logged:
            raise HTTPException(status_code=400, detail="Incorrect email or password")
        user = UserBase(**user_logged)
        hashed_password = self.verify_password(form_data.password, user.password)
        if not hashed_password:
            raise HTTPException(status_code=400, detail="Incorrect email or password")
        tokenjwt = TokenJWT()
        token = tokenjwt.create_access_token()
        return token
       
