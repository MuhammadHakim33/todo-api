from typing import Annotated, Union
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Optional
from models.model_todo import TodoModel
from models.model_user import RegisterModel, LoginModel, UserBase
from models.model_authCustom import OAuth2PasswordRequestFormCustom
from service.service_todo import TodoService
from service.service_user import UserService

route = APIRouter(prefix="/api/v1")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/login")

@route.post("/todos")
def store(
        todo: TodoModel, 
        service_todo: TodoService = Depends(), 
        token: str = Depends(oauth2_scheme)
    ):
    service_todo.store_todo(todo)
    return todo

@route.get("/todos")
def get(
        category: Optional[str] = None, 
        complete: Optional[bool] = None, 
        service_todo: TodoService = Depends(),
        token: str = Depends(oauth2_scheme)
    ):
    return service_todo.get_todo(category, complete)

@route.put("/todos/{todo_id}")
def update(
        todo_id: str, 
        todo: TodoModel, 
        service_todo: TodoService = Depends(),
        token: str = Depends(oauth2_scheme)
    ):
    return service_todo.update_todo(todo_id, todo)

@route.delete("/todos/{todo_id}")
def delete(
        todo_id: str, 
        service_todo: TodoService = Depends(),
        token: str = Depends(oauth2_scheme)
    ):
    return service_todo.delete_todo(todo_id)



@route.post("/register")
def register(user: RegisterModel, service_user: UserService = Depends()):
    result = service_user.register(user)
    return result

@route.post("/login")
def login(
        form_data: OAuth2PasswordRequestFormCustom = Depends(),
        service_user: UserService = Depends()
    ):
    token = service_user.login(form_data)
    return {"access_token": token, "token_type": "bearer"}
