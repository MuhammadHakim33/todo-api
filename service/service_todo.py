from fastapi import Depends
from models.model_todo import TodoModel
from repository.repository_todo import TodoRepository

class TodoService:
    def __init__(self, repo_todo: TodoRepository = Depends()):
        self.repo_todo = repo_todo

    def store_todo(self, todo: TodoModel):
        return self.repo_todo.store(todo)
    
    def get_todo(self, category : str | None = None):
        filter = {}
        if category is not None:
            filter["category"] = category
        return self.repo_todo.get(filter)