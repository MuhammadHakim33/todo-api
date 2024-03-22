from pydantic import BaseModel, EmailStr, Field, field_validator

class UserBase(BaseModel):
   id:str = Field(alias='_id')
   name:str
   email:str 

class LoginModel(BaseModel):
   email:str
   password:str

class RegisterModel(BaseModel):
   name:str
   email:EmailStr 
   password:str = Field(..., min_length=7)

   @field_validator('password')
   @classmethod
   def password_must_contain_alphanumeric(cls, v):
      if not any(char.isdigit() for char in v) or not any(char.isalpha() for char in v):
          raise ValueError("Password must contain both letters and numbers")
      return v