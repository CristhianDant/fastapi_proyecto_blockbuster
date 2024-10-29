from fastapi import APIRouter, Body , Depends , Path , Query , status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from config.database import Session

from .servise import PeliculasService , Peliculas

## Create a new router
peliculas_router = APIRouter()

@peliculas_router.get('/peliculas', tags=['peliculas'], status_code=status.HTTP_200_OK)
def get_peliculas():
    db = Session()
    result = PeliculasService(db).get_peliculas()
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result))

@peliculas_router.get('/pelicula/{idPelicula}', tags=['peliculas'], status_code=status.HTTP_200_OK)
def get_pelicula(idPelicula: int = Path(..., title='The ID of the pelicula')):
    db = Session()
    result = PeliculasService(db).get_pelicula(idPelicula)

    if not result:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'message': 'Pelicula not found'})
    
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result))
    

@peliculas_router.post('/pelicula', tags=['peliculas'], status_code=status.HTTP_201_CREATED)
def create_pelicula(pelicula: Peliculas):
    db = Session()
    result = PeliculasService(db).create_pelicula(pelicula)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder(result))


@peliculas_router.put('/pelicula/{idPelicula}', tags=['peliculas'], status_code=status.HTTP_200_OK)
def update_pelicula(idPelicula: int, pelicula: Peliculas):
    db = Session()
    result = PeliculasService(db).get_pelicula(idPelicula)
    if not result:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'message': 'Pelicula not found'})
    
    PeliculasService(db).update_pelicula(idPelicula, pelicula)
    return JSONResponse(status_code=status.HTTP_200_OK, content={'message': 'Pelicula updated'})


@peliculas_router.delete('/pelicula/{idPelicula}', tags=['peliculas'], status_code=status.HTTP_200_OK)
def delete_pelicula(idPelicula: int = Path(..., title='The ID of the pelicula')):
    db = Session()
    result = PeliculasService(db).get_pelicula(idPelicula)
    if not result:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'message': 'Pelicula not found'})
    
    PeliculasService(db).delete_pelicula(idPelicula)
    return JSONResponse(status_code=status.HTTP_200_OK, content={'message': 'Pelicula deleted'})

