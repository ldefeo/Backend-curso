Todas las APIS separadas funcionan como routers, para asi poder llamarlas desde main.

OJO! main tambien es una API, pero es la API master. O sea products y users, por ejemplo, van a trabajar como API's de la API general y main seria como la API controladora de la API general.


En APIRouter() hay una operacion que es prefix el cual me indica el prefijo que le quiera poner a las rutas de cada get, post, put y delete (generalmente suelen tener el mismo prefijo, asi queda mas prolijo).
                 -->   APIRouter(prefix="/users") por ejemplo
La / dentro de los get, post, put y delete indica el prefijo.

En APIRouter() tmb esta tags=["nombre del prefijo sin barra"] para indicar al swagger que no me junte las funciones de todas las API's, y me las separe por tags.


El response_model en cada get (por ejemplo) le indica al frontend que tipo de dato va a devolver la funcion de ese get. (IMPORTANTE)

EXCEPCIONES:
Con HTTPException() puedo setear el tipo de status_code que me va a devolver en caso de fallar y algun mensaje que le quiera tirar. (IMPORTANTE)
    #EXCEPCIONES: raise HTTPException(status_code=204,detail="El usuario ya existe") --->para lanzar excepciones con el codigo de error que queramos, el detail puede ir como no ir. 

AUTENTICACION BASICA:
OAuth2PasswordBearer ---> se encarga de gestionar la autenticacion (usuario y password). Se le pasa por parametro el tokenurl, ya que tokenurl es la url que se va a encargar de la autenticacion.

OAuth2PasswordRequestForm ---> es la forma en la que se va a enviar a nuestro backend api estos criterios de autenticacion. Es decir, es el que captura el usuario y password para enviarlos.

AUTENTICACION JWT:

Debemos como primer paso encriptar la contrasenia para asegurarla y que solo el servidor de desencriptacion conozca.

Debemos implementar en la funcion autenticar alguna operacion para saber si la contrasenia se ha verificado o no. Para eso debemos definir un contexto de encriptacion (la llamamos crypt).
Debemos encryptar la contrasenia en el db ---> utilizamos una pag de internet: https://bcrypt-generator.com/

Con la funcion crypt.verify(form.password,user.password) verifico si la contrasenia encriptada es la que debe ser (le paso la encriptada que es la de form, y le paso la original que es la de user) ----> NO PODEMOS DEVOLVER COMO ACCESS_TOKEN EL USERNAME PORQUE OBVIAMENTE TAMPOCO SERIA SEGURO.

Entonces debemos crear una autenticacion de forma segura. Se suele utilizar que el token se regenere una vez pasado la fecha de expiracion (para ello se utilizan fechas ---> se importa timedelta para trabajar con cuentas con fechas).

Encriptamos el token con jwt.encode(token,algorithm) donde el algorithm se elige.

**Se puede utilizar una clave que solo nosotros conocemos para encriptar y desencriptar lo que lo hace la forma mas segura de realizar esto** : Entonces creamos una variable global SECRET (le ponemos lo que sea) ---> para generarla podemos tirar el comando openssl rand -hex 32 (me va a devolver un numero random de 32 bit en hexadecimal)

Entonces, el metodo de encriptacion nos quedaria como jwt.encode(token,SECRET,algorithm)

Para obtener con get el usuario desencriptado, debemos desencriptarlo con los mismos parametros pero ahora con jwt.decode(token,SECRET,algorithms=[]).get("el parametro del json del token que tenga el username") 
