# ---- SERIA LO MISMO QUE USERS.PY PERO UTILIZANDO MONGODB ----
from fastapi import APIRouter, HTTPException
from db.client import db_client
from schemas.user_schema import User,UserUpdate
from typing import List
from db.models.user import user_model


router_user_db = APIRouter(prefix="/users_db",tags=["users_db"])

users_db = []

@router_user_db.get("/",response_model=List[User])
async def get_all_users():
    return users_db


@router_user_db.get("/{id}")
async def get_user(id:int):
    user = filter(lambda user: user.id == id,users_db)
    return list(user) 


@router_user_db.get("/")
async def get_user_query(id:int):
    user = filter(lambda user: user.id == id,users_db)
    return list(user) 


@router_user_db.get("/")
async def get_user_query2(id:int,name:str):
    user = filter(lambda user: (user.id == id)and(user.name == name),users_db)
    return list(user) 


# POSTS
# --- Debemos generar la funcion post para agregar usuarios a nuestra base de datos ---

@router_user_db.post("/",status_code=201) 
async def agregar_user(user: User):
    user_dict = dict(user) #transformo mi usuario en un diccionario
    del user_dict["id"] #si el campo id no llega con la peticion, entonces que el mongodb lo genere automaticamente
    
    #el id debe ser de tipo string
    id = db_client.local.users.insert_one(user_dict).inserted_id #accedo a local de la base de datos, genero una tabla users e inserto un user (en formato json)
                                            #tmb esta insert_many() para insertar varios users 
                                            #Luego, accedo al id que inserto mongodb
    new_user = user_model(db_client.local.users.find_one({"_id": id})) #se lo mando a user_model 
                                    #para que me devuelva el objeto en el formato que indica la funcion
    
    return User(**new_user) #me devuelve un objeto de tipo usuario con todos los campos

#PUTS

@router_user_db.put("/")
async def cambiar_user_entero(user:User):
    for index,user_i in enumerate(users_db): 
        if(user_i.id == user.id):
            users_db[index] = user_i

@router_user_db.put("/update/user", status_code=200) 
def update_user(user: UserUpdate):
    for user_i in users_db:
        if(user_i.id == user.id):
            for atributo, valor in user.dict(exclude_none=True).items():  
                setattr(user_i, atributo, valor)
                return {"detail": "The user update successfully"}
    raise HTTPException(status_code=400, detail="The user not exist.")
            
@router_user_db.put("/edad/")
def cambiar_edad(id:int,age:int):
    for user in users_db:
        if(user.id == id):
            user.age = age

#DELETE

@router_user_db.delete("/{id}")
async def delete_user(id:int):
    for index, user_i in enumerate(users_db):
        if(user_i.id == id):
            del users_db[index]