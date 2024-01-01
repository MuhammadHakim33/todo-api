from fastapi import Depends
from bson.objectid import ObjectId
from models.model_todo import TodoModel
from repository.repository_todo import TodoRepository
from typing import Optional

class TodoService:
    def __init__(self, repo_todo: TodoRepository = Depends()):
        self.repo_todo = repo_todo

    def store_todo(self, todo: TodoModel):
        return self.repo_todo.store(todo)
    
    def get_todo(self, category: Optional[str] = None):
        filter = {}
        if category is not None:
            filter["category"] = category
        return self.repo_todo.get(filter)
    
    def update_todo(self, todo_id: str, todo: TodoModel):
        oldData = self.repo_todo.get_one({"_id": ObjectId(todo_id)})
        newData = {
            "name": todo.name if todo.name != "string" else oldData["name"],
            "category": todo.category if todo.category != "string" else oldData["category"],
            "complete": oldData["complete"],
        }
        return self.repo_todo.update(todo_id, newData)
    
    def delete_todo(self, todo_id: str):
        oldData = self.repo_todo.get_one({"_id": ObjectId(todo_id)})
        return self.repo_todo.delete(oldData["_id"])