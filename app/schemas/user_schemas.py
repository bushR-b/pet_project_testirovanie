from typing import Optional
from pydantic import BaseModel


class UserLogin(BaseModel):
    username: str 
    password: str 

class UserRegister(BaseModel):
    name: str 
    surname: str 
    last_name: str 
    username: str 
    password: str 
    confirm_password: str 

class UserPublic(BaseModel):
    name: str 
    surname: str 
    last_name: str 
    username: str   

class UserRefresh(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    last_name: Optional[str] = None
