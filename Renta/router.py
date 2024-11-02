from fastapi import APIRouter , Depends , Path , Query , status , Body
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from config.database import Session
from .servise import RentaServise , Renta_encabezado , Renta_detalle

## Create a new router
renta_router = APIRouter()

@renta_router.get('/rentas', tags=['rentas'], status_code=200)
def get_rentas():
    db = Session()
    result = RentaServise(db).get_list_rentas_between_dates()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@renta_router.get('/rentas/{idRenta_enc}', tags=['rentas'], status_code=status.HTTP_200_OK)
def get_renta(idRenta_enc:int):
    db = Session()
    result = RentaServise(db).get_renta(idRenta_enc)
    
    if not result["renta_enc"]:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Renta no encontrada"})
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result))


@renta_router.post('/rentas', tags=['rentas'], status_code=status.HTTP_201_CREATED)
def create_renta(renta_enc: Renta_encabezado = Body(), detalle: list[Renta_detalle] = Body()):
    db = Session()
    RentaServise(db).create_renta(renta_enc, detalle)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED, 
        content={"message": "Renta creada"}
    )

@renta_router.put('/rentas/{idRenta_enc}', tags=['rentas'], status_code=status.HTTP_200_OK)
def update_renta(idRenta_enc:int, renta_enc: Renta_encabezado = Body()):
    db = Session()
    RentaServise(db).update_renta(idRenta_enc, renta_enc)
    
    return JSONResponse(
        status_code=status.HTTP_200_OK, 
        content={"message": "Renta actualizada"}
    )

@renta_router.delete('/rentas/{idRenta_enc}', tags=['rentas'], status_code=status.HTTP_200_OK)
def delete_renta(idRenta_enc:int):
    db = Session()
    RentaServise(db).delete_renta(idRenta_enc)
    
    return JSONResponse(
        status_code=status.HTTP_200_OK, 
        content={"message": "Renta eliminada"}
    )

@renta_router.get('/ultima_renta', tags=['rentas'], status_code=status.HTTP_200_OK)
def get_ultima_renta():
    db = Session()
    result = RentaServise(db).get_ulitma_renta()
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder({"idRenta_enc": result}))

@renta_router.put('/finalizar_renta/{idRenta_enc}', tags=['rentas'], status_code=status.HTTP_200_OK)
def finalizar_renta(idRenta_enc:int):
    db = Session()
    RentaServise(db).finalizar_renta(idRenta_enc=idRenta_enc)
    
    return JSONResponse(
        status_code=status.HTTP_200_OK, 
        content={"message": "Renta finalizada"}
    )


