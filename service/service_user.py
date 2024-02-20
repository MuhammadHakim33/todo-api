from fastapi import Depends, HTTPException
from models.model_user import RegisterModel, LoginModel
from repository.repository_user import UserRepository
from passlib.context import CryptContext

class UserService:
    def __init__(self, repo_user: UserRepository = Depends()):
        self.repo_user = repo_user
        self.pwd_context = CryptContext(schemes=["sha256_crypt"])

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
    
    def login(self, user: LoginModel):
        return self.repo_user.find(user)
       
