

from fastapi import APIRouter , Depends , Path , Query , status 
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List

from config.database import Session
from .servise import ClientService , Cliente 
from middlewares.JWT_bearer import JWTBearer
## Create a new router
cliente_router = APIRouter()

@cliente_router.get('/clientes', tags=['clientes'], 
    status_code=status.HTTP_200_OK,
    response_model=List[Cliente]
    )
def get_clientes():
    """
    Endpoint para obtener un listado de clientes registrados
    """
    db = Session()
    result = ClientService(db).get_clientes()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@cliente_router.get('/clientes/{idCliente}', tags=['clientes'],
        status_code=status.HTTP_200_OK , 
        response_model=Cliente)
def get_cliente(idCliente:int = Path(... , ge=1 , examples=[1, 2, 3])):
    db = Session()
    result = ClientService(db).get_cliente(idCliente)
    
    if not result:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Cliente no encontrado"})
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result))

@cliente_router.get('/clientes/', tags=['clientes']
    ,status_code=status.HTTP_200_OK
    ,response_model=Cliente)
def get_cliente_by_name(nombre:str):
    db = Session()
    result = ClientService(db).get_cliente_by_name(nombre)
    if not result:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Cliente no encontrado"})
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result))

@cliente_router.post('/clientes', tags=['clientes'], 
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(JWTBearer())])
def create_cliente(cliente: Cliente) -> JSONResponse:
    """
    Endpoint para crear un nuevo cliente

    Args:
        cliente (Cliente): Información del cliente a crear
    Returns:
        JSONResponse: Mensaje de éxito
    """
    db = Session()
    ClientService(db).create_cliente(cliente)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED, 
        content={"message": f"Cliente {cliente.nombre} creado con {cliente.idCliente}"})



@cliente_router.put('/clientes/{idCliente}', tags=['clientes'], 
                    status_code=status.HTTP_200_OK,
                    dependencies=[Depends(JWTBearer())])
def update_cliente(idCliente:int, cliente: Cliente) -> dict:
    """
    Endpoint para actualizar un cliente
    Args:
        idCliente (int): ID del cliente
        cliente (Cliente): Información del cliente a actualizar
    Returns:
        JSONResponse: Mensaje de éxito
    """
    db = Session()
    result = ClientService(db).get_cliente(idCliente)
    if not result:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Cliente no encontrado"})
    ClientService(db).update_cliente(idCliente, cliente)
    return JSONResponse(
        status_code=status.HTTP_200_OK, 
        content={"message": f"Cliente {cliente.nombre} actualizado con éxito"})



@cliente_router.delete('/clientes/{idCliente}', 
                    tags=['clientes'], status_code=status.HTTP_200_OK,
                    dependencies=[Depends(JWTBearer())])
def delete_cliente(idCliente:int) -> dict:
    """
    Endpoint para eliminar un cliente
    Args:
        idCliente (int): ID del cliente
    Returns:
        JSONResponse: Mensaje de éxito
    """
    db = Session()
    result = ClientService(db).get_cliente(idCliente)
    if not result:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Cliente no encontrado"})
    ClientService(db).delete_cliente(idCliente)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Cliente eliminado"})