from pymongo.database import Database
from fastapi import Depends
from config.db import db_conn
from models.model_user import RegistrationModel, LoginModel

class UserRepository:
    def __init__(self, db: Database = Depends(db_conn)):
        self.repository = db.users

    def create(self, user: RegistrationModel):
        return self.repository.insert_one(user.model_dump())
    
    def find(self, user: LoginModel):
        result = self.repository.find_one({
            "email" : user.email,
            "password" : user.password
        })
        if result is None:
            return None
        return user.model_validate(result)
    
