from bson.objectid import ObjectId
from config.db import db_conn
from models.model_todo import TodoModel

class TodoRepository:
    def __init__(self):
        self.repository = db_conn().todo

    def store(self, todo: TodoModel):
        return self.repository.insert_one(todo.model_dump())
    
    def get(self, filter: dict):
        result = []
        data = list(self.repository.find(filter))
        for document in data:
            document["_id"] = str(document["_id"])
            result.append(TodoModel(**document))
        return data
    
    def get_one(self, filter: dict):
        return self.repository.find_one(filter)
    
    def update(self, todo_id: str, todo: TodoModel):
        self.repository.update_one({"_id": ObjectId(todo_id)}, {"$set": todo})
        return {"response": "success"}
    
    def delete(self, todo_id: str):
        self.repository.delete_one({"_id": ObjectId(todo_id)})
        return {"response": "success"}
