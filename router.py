from fastapi import APIRouter, Depends, Form
from typing import Optional
from models.model_authCustom import OAuth2PasswordRequestFormCustom
from models.model_todo import TodoModel
from models.model_user import RegisterModel, UserBase
from models.model_token import Token
from service.service_todo import TodoService
from service.service_auth import create_user, auth, verified_user
from service.service_token import create_access_token

route = APIRouter(prefix="/api/v1")


@route.post("/todos", response_model=TodoModel)
def store(
        name: str = Form(), category: str = Form(), complete: bool = Form(),
        service_todo: TodoService = Depends(), 
        user: UserBase = Depends(verified_user)
    ):
    todo = TodoModel(name=name, category=category, complete=complete, user_id=user.id)
    service_todo.store_todo(todo)
    return todo

@route.get("/todos")
def get(
        category: Optional[str] = None, 
        complete: Optional[bool] = None, 
        service_todo: TodoService = Depends(),
        user: UserBase = Depends(verified_user)
    ):
    # print(verified)
    # return True
    return service_todo.get_todo(category, complete, user.id)

@route.put("/todos/{todo_id}")
def update(
        todo_id: str, 
        todo: TodoModel, 
        service_todo: TodoService = Depends(),
        user: UserBase = Depends(verified_user)
    ):
    return service_todo.update_todo(todo_id, todo)

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
def login(form_data: OAuth2PasswordRequestFormCustom = Depends()):
    user = auth(form_data)
    access_token = create_access_token(data={"sub": user.email})
    return Token(access_token=access_token, token_type="bearer")
