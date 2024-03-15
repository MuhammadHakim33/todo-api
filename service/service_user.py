from fastapi import Depends
from repository.repository_user import UserRepository

class UserService:
    def __init__(self, repo_user: UserRepository = Depends()):
        self.repo_user = repo_user
