from fastapi import APIRouter
### ES UNA API SEPARADA DE LA DE USERS.PY, SE DEBE INICIAR CON UVICORN PRODUCTOS:APP --RELOAD COMO CON USERS. O SEA
### SE DEBEN ARRANCAR DESDE EL MAIN PARA QUE NO TENGAMOS QUE USAR LA TERMINAL SIEMPRE

router_product = APIRouter(prefix="/productos",tags=["productos"])

productos = ["P1","P2","P3","P4","P5"]


@router_product.get("/")
async def get_all_products():
    return productos

@router_product.get("/{id}")
async def get_product(id: int):
    return productos[id]

