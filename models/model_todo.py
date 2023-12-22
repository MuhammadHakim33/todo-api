from pydantic import BaseModel

class TodoModel(BaseModel):
   name:str
   category:str
   complete:bool = False