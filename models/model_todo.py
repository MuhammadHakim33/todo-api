from pydantic import BaseModel, Field

class TodoModel(BaseModel):
   id:str = Field(alias='_id')
   name:str
   category:str
   complete:bool = False
   user_id:str