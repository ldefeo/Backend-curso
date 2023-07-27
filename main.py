from fastapi import FastAPI
from routers import productos,users,basic_auth_users,jwt_auth_users,users_db
from fastapi.staticfiles import StaticFiles

"""Swagger: http://127.0.0.1:8000/docs"""
"""CORRER: uvicorn main:app --reload"""

app = FastAPI()

#ROUTERS
app.include_router(productos.router_product) ### ---> importamos el router de productos para poder iniciarlo
app.include_router(users.router_user) ### ---> lo mismo con users
app.include_router(basic_auth_users.router_auth)
app.include_router(jwt_auth_users.router_auth_jwt)
app.include_router(users_db.router_user_db)

app.mount("/statics",StaticFiles(directory="statics"),name="statics") ### ---> llamo al directorio que llame statics para poder utilizarlo en la ruta de google y asi ver lo que hay dentro

@app.get("/") #accedemos a app que la creamos en la linea 3. Obtenemos con get algo que esta en el lugar indicado en el corchete (en este caso solo /)
async def root(): #asincrona porque asi le indicamos que haga lo que tenga que hacer cuando pueda
    return "Hola FastAPI"

@app.get("/url")
async def url():
    return {"url":"google.com"}