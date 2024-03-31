from fastapi import Depends, HTTPException
from bson.objectid import ObjectId
from bson.errors import InvalidId
from models.model_todo import NewTodo, UpdateTodo
from repository.repository_todo import TodoRepository
from typing import Optional

class TodoService:
    def __init__(self, repo_todo: TodoRepository = Depends()):
        self.repo_todo = repo_todo

    def store_todo(self, todo: NewTodo, user_id: str):
        data = todo.model_dump()
        data.update({"user_id": ObjectId(user_id)})
        return self.repo_todo.store(data)
    
    def get_todo(self, 
                 category: Optional[str] = None, 
                 complete: Optional[bool] = None,
                 user: Optional[str] = None
        ):
        filter = {}
        if category is not None:
            filter["category"] = category
        if complete is not None:
            filter["complete"] = complete
        if user is not None:
            filter["user_id"] = ObjectId(user)
        return self.repo_todo.get(filter)
    
    def update_todo(self, todo: UpdateTodo):
        try: 
            dataOld = self.repo_todo.get_one({"_id": ObjectId(todo.id)})
            data = UpdateTodo(**dataOld)
            if todo.name is not None:
                data.name = todo.name
            if todo.category is not None:
                data.category = todo.category
            if todo.complete is not None:
                data.complete = todo.complete
            if todo.due is not None:
                data.due = todo.due
        except InvalidId:
            raise HTTPException(status_code=404, detail="Todo Not Found")
        
        return self.repo_todo.update(data)
    
    def delete_todo(self, todo_id: str):
        try: 
            dataOld = self.repo_todo.get_one({"_id": ObjectId(todo_id)})
        except InvalidId:
            raise HTTPException(status_code=404, detail="Todo Not Found")
        
        return self.repo_todo.delete(dataOld["_id"])