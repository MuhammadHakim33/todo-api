from fastapi import APIRouter, Depends
from typing import Optional, Annotated
from models.model_authCustom import OAuth2PasswordRequestFormCustom
from models.model_todo import TodoModel
from models.model_user import RegisterModel, UserBase
from models.model_token import Token
from service.service_todo import TodoService
from service.service_auth import register, auth, verified_user
from service.service_token import create_access_token

route = APIRouter(prefix="/api/v1")


@route.post("/todos")
def store(
        todo: TodoModel, 
        service_todo: TodoService = Depends(), 
        verified: UserBase = Depends(verified_user)
    ):
    service_todo.store_todo(todo)
    return todo

@route.get("/todos")
def get(
        category: Optional[str] = None, 
        complete: Optional[bool] = None, 
        service_todo: TodoService = Depends(),
        verified: UserBase = Depends(verified_user)
    ):
    return service_todo.get_todo(category, complete)

@route.put("/todos/{todo_id}")
def update(
        todo_id: str, 
        todo: TodoModel, 
        service_todo: TodoService = Depends(),
        verified: UserBase = Depends(verified_user)
    ):
    return service_todo.update_todo(todo_id, todo)

@route.delete("/todos/{todo_id}")
def delete(
        todo_id: str, 
        service_todo: TodoService = Depends(),
        verified: UserBase = Depends(verified_user)
    ):
    return service_todo.delete_todo(todo_id)



@route.post("/register")
def register(user: RegisterModel):
    result = register(user)
    return result

@route.post("/login")
def login(form_data: OAuth2PasswordRequestFormCustom = Depends()):
    user = auth(form_data)
    access_token = create_access_token(data={"sub": user.email})
    return Token(access_token=access_token, token_type="bearer")
