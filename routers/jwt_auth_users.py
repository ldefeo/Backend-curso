from fastapi import APIRouter, Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from schemas.user_schema import UserAuth, UserDB
from db.user_db import users_db_auth
from jose import jwt,JWTError
from passlib.context import CryptContext
from datetime import datetime,timedelta

ALGORITHM = "HS256" ##---> TIPO DE ALGORITMO QUE SE PUEDE UTILIZAR PARA ENCRIPTAR LA CONTRASENIA
ACCESS_TOKEN_DURATION = 1
SECRET = "61cfed83b335d3a4c3f99acd0dd60887bb577fd821823173025b7daf2eaa36cd"

router_auth_jwt = APIRouter(prefix="/login_jwt",tags=["login_jwt"])

oauth2 = OAuth2PasswordBearer(tokenUrl= "login_jwt") 
crypt = CryptContext(schemes=["bcrypt"])


def search_user_db(username: str):
    if(username in users_db_auth): #si el username se encuentra en la db, recupero el usuario y lo devuelvo como un usuario db
        return UserDB(**users_db_auth[username])

def search_user(username: str):
    if(username in users_db_auth):
        return UserAuth(**users_db_auth[username])
    
def auth_user(token: str = Depends(oauth2)):  #---> debemos encontrar el usuario que esta autenticado
    exception = HTTPException(status_code=404,detail="El usuario no esta autorizado")
    try:
        username = jwt.decode(token,SECRET,algorithms=[ALGORITHM]).get("sub") 
        if username is None:
            raise exception
    except JWTError:
        raise exception
    
    return search_user(username)
    
def current_user(user: UserAuth = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(status_code=400,detail="Usuario inactivo")
    return user

@router_auth_jwt.post("/login") #para autenticarse
def autenticar(form: OAuth2PasswordRequestForm = Depends()): #el form depende de algo (username y password seria)
    user_db = users_db_auth.get(form.username)
    if not user_db:
        raise HTTPException(status_code=400,detail="El usuario no es correcto")
    
    user = search_user_db(form.username) #nos va a devolver un usuario db con password y ahora si puedo chequearla
    
    if not crypt.verify(form.password,user.password): 
        raise HTTPException(status_code=400,detail="La password no es correcta")

    access_token_expiration = timedelta(minutes=ACCESS_TOKEN_DURATION) #---> va a crear un delta que sea de 1 minuto mas de lo que nosotros tenemos

    expire = datetime.utcnow() + access_token_expiration #con utcnow me da la fecha, hora, etc que es en este momento.
                                                        #le tengo que sumar el minuto que agregamos como delta para saber si expiro
    access_token = {"sub":user.username, "exp":expire} #ESTO IGUAL TIENE QUE ENCRIPTARSE

    return {"access_token": jwt.encode(access_token,SECRET,algorithm=ALGORITHM),"token_type" : "bearer"}


@router_auth_jwt.get("/users/me")
def me(user: UserAuth = Depends(current_user)): #el user depende de si esta autenticado o no
    return user

