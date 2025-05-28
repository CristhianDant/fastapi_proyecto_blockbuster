from fastapi import APIRouter, Body , Depends , Path , Query , status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from config.database import Session
from .servise import PersonalService , Personal 
from middlewares.JWT_bearer import JWTBearer    
from .models import UpdatePasswordRequest


## Create a new router
personal_router = APIRouter()  

@personal_router.get('/personals', tags=['personals'], status_code=200)
def get_personals():
    db = Session()
    result = PersonalService(db).get_personals()

    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@personal_router.get('/personal/{idPersonal}', tags=['personals'], status_code=200)
def get_personal(idPersonal: int = Path(..., title='The ID of the personal')):
    db = Session()
    result = PersonalService(db).get_personal(idPersonal)
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@personal_router.post('/personal', tags=['personals'], 
    status_code=status.HTTP_201_CREATED)
def create_personal(personal: Personal):
    db = Session()
    result = PersonalService(db).create_personal(personal)
    return JSONResponse(status_code=201, content=jsonable_encoder(result))


@personal_router.put('/personal/{idPersonal}', tags=['personals'],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(JWTBearer())])
def update_personal(idPersonal: int, personal: Personal):
    db = Session()
    result = PersonalService(db).get_personal(idPersonal)
    if not result:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'message': 'Personal not found'})
    
    print(f'{personal}')
    PersonalService(db).update_personal(idPersonal, personal)
    return JSONResponse(status_code=status.HTTP_200_OK, content={'message': 'Personal updated'})


@personal_router.put('/personal/password', tags=['personals'],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(JWTBearer())])
def update_password(data: UpdatePasswordRequest):
    db = Session()
    result = PersonalService(db).update_password(data.model_dump())
    if not result:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'message': 'Personal not found'})
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result))


@personal_router.delete('/personal/{idPersonal}', tags=['personals'],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(JWTBearer())])
def delete_personal(idPersonal: int):
    db = Session()
    result = PersonalService(db).get_personal(idPersonal)
    if not result:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'message': 'Personal not found'})
    PersonalService(db).delete_personal(idPersonal)
    return JSONResponse(
        status_code=status.HTTP_200_OK, 
        content={'message': 'Personal deleted'}
    )