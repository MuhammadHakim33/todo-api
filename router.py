from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from models.model_todo import TodoModel
from models.model_user import RegistrationModel, LoginModel
from service.service_todo import TodoService
from service.service_user import UserService

route = APIRouter(prefix="/api/v1")

@route.post("/todos")
def store(todo: TodoModel, service_todo: TodoService = Depends()):
    service_todo.store_todo(todo)
    return todo

@route.get("/todos")
def get(category: Optional[str] = None, complete: Optional[bool] = None, service_todo: TodoService = Depends()):
    return service_todo.get_todo(category, complete)

@route.put("/todos/{todo_id}")
def update(todo_id: str, todo: TodoModel, service_todo: TodoService = Depends()):
    return service_todo.update_todo(todo_id, todo)

@route.delete("/todos/{todo_id}")
def delete(todo_id: str, service_todo: TodoService = Depends()):
    return service_todo.delete_todo(todo_id)



@route.post("/user/registration")
def registration(user: RegistrationModel, service_user: UserService = Depends()):
    service_user.registration(user)
    return user

@route.post("/user/login")
def login(user: LoginModel, service_user: UserService = Depends()):
    result = service_user.login(user)
    if result is None:
        raise HTTPException(401, "INVALID EMAIL OR PASSWORD")
    return result