from fastapi import Depends, HTTPException
from models.model_user import RegisterModel, LoginModel, UserBase
from repository.repository_user import UserRepository
from passlib.context import CryptContext
import uuid

class UserService:
    def __init__(self, repo_user: UserRepository = Depends()):
        self.repo_user = repo_user
        self.pwd_context = CryptContext(schemes=["sha256_crypt"])

    def generate_token(self):
        token = uuid.uuid4()
        return str(token)

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
    
    def login(self, form_data: LoginModel):
        user_logged = self.repo_user.find({'email': form_data.email})
        if not user_logged:
            raise HTTPException(status_code=400, detail="Incorrect email or password")
        user = UserBase(**user_logged)
        hashed_password = self.verify_password(form_data.password, user.password)
        if not hashed_password:
            raise HTTPException(status_code=400, detail="Incorrect email or password")
        token = self.generate_token()
        return token
       
