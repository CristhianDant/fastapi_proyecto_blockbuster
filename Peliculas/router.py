from fastapi import APIRouter, Body , Depends , Path , Query , status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from config.database import Session
from middlewares.JWT_bearer import JWTBearer
from .servise import PeliculasService , Peliculas


## Create a new router
peliculas_router = APIRouter()

@peliculas_router.get('/peliculas', tags=['peliculas'],
    status_code=status.HTTP_200_OK, 
    response_model=list[Peliculas])
def get_peliculas():
    """
    Endpoint para obtener todas las peliculas
    """
    db = Session()
    result = PeliculasService(db).get_peliculas()
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result))

@peliculas_router.get('/pelicula/{idPelicula}', tags=['peliculas'], 
    status_code=status.HTTP_200_OK,
    response_model=Peliculas)
def get_pelicula(idPelicula: int = Path(..., title='The ID of the pelicula', ge=1)):
    db = Session()
    result = PeliculasService(db).get_pelicula(idPelicula)

    if not result:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'message': 'Pelicula not found'})
    
    return JSONResponse(status_code=status.HTTP_200_OK, 
        content=jsonable_encoder(result))
    

@peliculas_router.post('/pelicula', tags=['peliculas'],
    status_code=status.HTTP_201_CREATED, 
    dependencies=[Depends(JWTBearer())])
def create_pelicula(pelicula: Peliculas) -> dict:
    """
    Endpoint para crear una nueva pelicula
    Args:
        pelicula (Peliculas): Pelicula a crear
    Returns:
        JSONResponse: Respuesta de la creacion de la pelicula
    """
    db = Session()
    result = PeliculasService(db).create_pelicula(pelicula)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=jsonable_encoder({
            'message': f'Pelicula {pelicula.nombre} creada'
        }))


@peliculas_router.put('/pelicula/{idPelicula}', tags=['peliculas'],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(JWTBearer())])
def update_pelicula(idPelicula: int, pelicula: Peliculas) -> JSONResponse:
    """
    Endpoint para modificar una pelicula
    Args:
        idPelicula (int): ID de la pelicula a modificar
        pelicula (Peliculas): Pelicula a modificar
    Returns:
        JSONResponse: Respuesta de la modificacion de la pelicula
    """
    db = Session()
    result = PeliculasService(db).get_pelicula(idPelicula)
    if not result:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'message': 'Pelicula not found'})
    
    PeliculasService(db).update_pelicula(idPelicula, pelicula)
    return JSONResponse(
        status_code=status.HTTP_200_OK, 
        content={'message': f'Pelicula {pelicula.nombre} modificada'})


@peliculas_router.delete('/pelicula/{idPelicula}', tags=['peliculas'], 
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(JWTBearer())])
def delete_pelicula(idPelicula: int = Path(..., title='The ID of the pelicula')):
    """
    Endpoint para eliminar una pelicula
    Args:
        idPelicula (int): ID de la pelicula a eliminar
    Returns:
        JSONResponse: Respuesta de la eliminacion de la pelicula
    """
    db = Session()
    result = PeliculasService(db).get_pelicula(idPelicula)
    if not result:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'message': 'Pelicula not found'})
    
    PeliculasService(db).delete_pelicula(idPelicula)
    return JSONResponse(
        status_code=status.HTTP_200_OK, 
        content={'message': 'Pelicula eliminada'})

