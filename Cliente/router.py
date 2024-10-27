# ffrom fastapi import APIRouter
# from fastapi import Depends, Path, Query
# from fastapi.responses import JSONResponse
# from pydantic import BaseModel, Field
# from typing import Optional, List
# from config.database import Session
# from models.movie import Movie as MovieModel
# from fastapi.encoders import jsonable_encoder
# from middlewares.jwt_bearer import JWTBearer
# from services.movie import MovieService



from fastapi import APIRouter , Depends , Path , Query , status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from config.database import Session
from .servise import ClientService , Cliente 
## Create a new router
cliente_router = APIRouter()

@cliente_router.get('/clientes', tags=['clientes'], status_code=200)
def get_clientes():
    db = Session()
    result = ClientService(db).get_clientes()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@cliente_router.get('/clientes/{idCliente}', tags=['clientes'], status_code=status.HTTP_200_OK)
def get_cliente(idCliente:int):
    db = Session()
    result = ClientService(db).get_cliente(idCliente)
    
    if not result:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Cliente no encontrado"})
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result))

@cliente_router.get('/clientes/', tags=['clientes'], status_code=status.HTTP_200_OK)
def get_cliente_by_name(nombre:str):
    db = Session()
    result = ClientService(db).get_cliente_by_name(nombre)
    if not result:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Cliente no encontrado"})
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result))

@cliente_router.post('/clientes', tags=['clientes'], status_code=status.HTTP_201_CREATED)
def create_cliente(cliente: Cliente):
    db = Session()
    ClientService(db).create_cliente(cliente)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED, 
        content={"message": "Cliente creado"})



@cliente_router.put('/clientes/{idCliente}', tags=['clientes'], status_code=status.HTTP_200_OK)
def update_cliente(idCliente:int, cliente: Cliente):
    db = Session()
    result = ClientService(db).get_cliente(idCliente)
    if not result:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Cliente no encontrado"})
    ClientService(db).update_cliente(idCliente, cliente)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Cliente actualizado"})

@cliente_router.delete('/clientes/{idCliente}', tags=['clientes'], status_code=status.HTTP_200_OK)
def delete_cliente(idCliente:int):
    db = Session()
    result = ClientService(db).get_cliente(idCliente)
    if not result:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Cliente no encontrado"})
    ClientService(db).delete_cliente(idCliente)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Cliente eliminado"})