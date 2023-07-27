from fastapi import APIRouter, Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from schemas.user_schema import UserAuth, UserDB
from db.user_db import users_db_auth_basic


router_auth = APIRouter(prefix="/login",tags=["login"])

oauth2 = OAuth2PasswordBearer(tokenUrl= "login") 


def search_user_db(username: str):
    if(username in users_db_auth_basic): #si el username se encuentra en la db, recupero el usuario y lo devuelvo como un usuario db
        return UserDB(**users_db_auth_basic[username])

def search_user(username: str):
    if(username in users_db_auth_basic):
        return UserAuth(**users_db_auth_basic[username])

def current_user(token: str = Depends(oauth2)):
    user = search_user(token) #porque el token coincide con el user name de la db
    if not user:
        raise HTTPException(status_code=404,detail="El usuario no esta autorizado")
    if user.disabled:
        raise HTTPException(status_code=400,detail="Usuario inactivo")
    return user
    
@router_auth.post("/login") #para autenticarse
def autenticar(form: OAuth2PasswordRequestForm = Depends()): #el form depende de algo (username y password seria)
    user_db = users_db_auth_basic.get(form.username)
    if not user_db:
        raise HTTPException(status_code=400,detail="El usuario no es correcto")
    
    user = search_user_db(form.username) #nos va a devolver un usuario db con password y ahora si puedo chequearla
    if not form.password == user.password:
        raise HTTPException(status_code=400,detail="La password no es correcta")

    return {"access_token": user.username,"token_type" : "bearer"}

@router_auth.get("/users/me")
def me(user: UserAuth = Depends(current_user)): #el user depende de si esta autenticado o no
    return user

