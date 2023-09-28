from fastapi import APIRouter, Depends
from models.model_todo import TodoModel
from service.service_todo import TodoService

route = APIRouter(prefix="/api/v1")

@route.post("/todos")
def store(todo: TodoModel, service_todo: TodoService = Depends()):
    service_todo.store_todo(todo)
    return todo

@route.get("/todos")
def get(category : str | None = None, service_todo: TodoService = Depends()):
    return service_todo.get_todo(category)