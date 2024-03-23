from typing import Optional
from pydantic import BaseModel, Field

class BaseTodo(BaseModel):
   id:str = Field(alias='_id')
   name:str
   category:str
   complete:bool = False
   user_id:str

class NewTodo(BaseModel):
   name:str
   category:str
   complete:bool = False

class UpdateTodo(BaseModel):
   id:str = Field(alias='_id')
   name: Optional[str] = None
   category: Optional[str] = None
   complete: Optional[bool] = None