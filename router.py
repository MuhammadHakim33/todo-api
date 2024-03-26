from fastapi import APIRouter, Depends
from typing import Optional
from models.model_todo import NewTodo, UpdateTodo
from models.model_user import LoginModel, RegisterModel, UserBase
from models.model_token import Token
from service.service_todo import TodoService
from service.service_auth import create_user, auth, verified_user
from service.service_token import create_access_token

route = APIRouter(prefix="/api/v1")

@route.get("/todos")
def get(
        category: Optional[str] = None, 
        complete: Optional[bool] = None, 
        service_todo: TodoService = Depends(),
        user: UserBase = Depends(verified_user)
    ):
    return service_todo.get_todo(category, complete, user.id)

@route.post("/todos")
def store(
        todo: NewTodo,
        service_todo: TodoService = Depends(), 
        user: UserBase = Depends(verified_user)
    ):
    return service_todo.store_todo(todo, user.id)

@route.put("/todos")
def update(
        todo: UpdateTodo, 
        service_todo: TodoService = Depends(),
        user: UserBase = Depends(verified_user)
    ):
    return service_todo.update_todo(todo)

@route.delete("/todos/{todo_id}")
def delete(
        todo_id: str, 
        service_todo: TodoService = Depends(),
        user: UserBase = Depends(verified_user)
    ):
    return service_todo.delete_todo(todo_id)


@route.post("/register")
def register(user: RegisterModel):
    result = create_user(user)
    return result

@route.post("/login")
def login(form_data: LoginModel):
    user = auth(form_data)
    access_token = create_access_token(data={"sub": user.email})
    return Token(access_token=access_token, token_type="bearer")
