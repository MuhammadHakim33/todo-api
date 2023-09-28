from pymongo.database import Database
from fastapi import Depends
from config.db import db_conn
from models.model_todo import TodoModel

class TodoRepository:
    def __init__(self, db: Database = Depends(db_conn)):
        self.repository = db.todo

    def store(self, todo: TodoModel):
        return  self.repository.insert_one(todo.model_dump())
    
    def get(self, filter: dict):
        # result = []
        data = list(self.repository.find(filter))
        for document in data:
            document["_id"] = str(document["_id"])
            # result.append(TodoModel(**document))
        return data
