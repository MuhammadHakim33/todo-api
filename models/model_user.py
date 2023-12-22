from pydantic import BaseModel

class RegistrationModel(BaseModel):
   email:str
   password:str
   name:str

class LoginModel(BaseModel):
   email:str
   password:str