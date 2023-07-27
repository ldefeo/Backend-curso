from typing import Optional
from pydantic import BaseModel

class User(BaseModel): #HERENCIA EN PYTHON: La clase User hereda de BaseModel
    id: Optional[str]
    name: str
    surname: str
    age: int
    url: str
    
class UserUpdate(BaseModel):
    id: int
    name: Optional[str]
    surname: Optional[str]
    age: Optional[int]
    url: Optional[str]
    
class UserAuth(BaseModel): # ---> va a ir a traves de la red por eso no tiene password en su definicion
    username: str
    full_name: str
    email: str
    disabled: bool #---> me indica si el usuario esta habilitado o deshabilitado (porque lo borro o cosas asi)
    
class UserDB(UserAuth): #agrega la password
    password: str