from fastapi import Depends
from models.model_user import RegistrationModel, LoginModel
from repository.repository_user import UserRepository

class UserService:
    def __init__(self, repo_user: UserRepository = Depends()):
        self.repo_user = repo_user

    def registration(self, user: RegistrationModel):
        return self.repo_user.create(user)
    
    def login(self, user: LoginModel):
        return self.repo_user.find(user)
       
