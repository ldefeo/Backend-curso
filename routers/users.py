from fastapi import APIRouter, HTTPException
from db.user_db import users_db
from schemas.user_schema import User,UserUpdate
from typing import List

router_user = APIRouter(prefix="/users",tags=["users"])

#BaseModel para formar un cuerpo de solicitud

#GETTERS

@router_user.get("/",response_model=List[User])
async def get_all_users():
    return users_db

        #PARAMETROS POR PATH
@router_user.get("/{id}")
async def get_user(id:int):
    user = filter(lambda user: user.id == id,users_db)
    return list(user) 

        #PARAMETROS POR QUERY ---> http://127.0.0.1:8000/users/?id=1 o el valor que quieras
        #Suelen usarse parametros por query cuando los parametros pueden no ser fijos
@router_user.get("/")
async def get_user_query(id:int):
    user = filter(lambda user: user.id == id,users_db)
    return list(user) 

        ##PARAMETROS POR QUERY 2 ---> http://127.0.0.1:8000/users/?id=1&name="Laura" o el valor que quieras
@router_user.get("/")
async def get_user_query2(id:int,name:str):
    user = filter(lambda user: (user.id == id)and(user.name == name),users_db)
    return list(user) 


# POSTS

@router_user.post("/",status_code=201) ### ---> puedo decirle que me devuelva un 201 como simbolo de que se creo correctamente el usuario
async def agregar_user(user: User):
    users_db.append(user)
    

#PUTS

@router_user.put("/")
async def cambiar_user_entero(user:User):
    for index,user_i in enumerate(users_db): ### ---> enumero la lista para saber en que pos esta el usuario que matchee con el if
        if(user_i.id == user.id):
            users_db[index] = user_i

@router_user.put("/update/user", status_code=200) # en caso de que ande bien, devuelve 200 en el status_code
def update_user(user: UserUpdate):
    for user_i in users_db:
        if(user_i.id == user.id):
            for atributo, valor in user.dict(exclude_none=True).items(): ##--> exclude_none es para que cambie 
                                            # los parametros que quiero cambiar y deje intactos los otros parametros.
                setattr(user_i, atributo, valor)
                return {"detail": "The user update successfully"}
    raise HTTPException(status_code=400, detail="The user not exist.")
            
@router_user.put("/edad/")
def cambiar_edad(id:int,age:int):
    for user in users_db:
        if(user.id == id):
            user.age = age

#DELETE

@router_user.delete("/{id}")
async def delete_user(id:int):
    for index, user_i in enumerate(users_db):
        if(user_i.id == id):
            del users_db[index]