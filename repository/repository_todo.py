from bson.objectid import ObjectId
from fastapi import HTTPException
from config.db import db_conn
from models.model_todo import BaseTodo, NewTodo, UpdateTodo

class TodoRepository:
    def __init__(self):
        self.repository = db_conn().todo

    def store(self, data: dict):
        self.repository.insert_one(data)
        return {"response": "success"} 
    
    def get(self, filter: dict):
        result = []
        data = list(self.repository.find(filter))
        for document in data:
            document["_id"] = str(document["_id"])
            document["user_id"] = str(document["user_id"])
            result.append(BaseTodo(**document))
        return result
    
    def get_one(self, filter: dict):
        data = self.repository.find_one(filter)
        if not data:
            raise HTTPException(status_code=404, detail="Todo Not Found")
        data["_id"] = str(data["_id"])
        return data
    
    def update(self, data: UpdateTodo):
        self.repository.update_one({"_id": ObjectId(data.id)}, {"$set": data.model_dump(exclude={'id'})})
        print(type(ObjectId(data.id)))
        return {"response": "success"}
    
    def delete(self, todo_id: str):
        self.repository.delete_one({"_id": ObjectId(todo_id)})
        return {"response": "success"}
