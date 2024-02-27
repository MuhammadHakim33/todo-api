from config.db import db_conn
from models.model_user import UserBase

class UserRepository:
    def __init__(self):
        self.repository = db_conn().users

    def find(self, filter: dict):
        result = self.repository.find_one(filter)
        return result

    def create(self, user: UserBase):
        self.repository.insert_one(user.model_dump())
        return {"message": "User registration successful", "data": user.model_dump(exclude='password')}