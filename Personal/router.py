from fastapi import APIRouter , Depends , Path , Query , status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from config.database import Session
from .servise import PersonalService , Personal 


## Create a new router
personal_router = APIRouter()  

@personal_router.get('/personals', tags=['personals'], status_code=200)
def get_personals():
    db = Session()
    result = PersonalService(db).get_personals()

    print(f'')
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@personal_router.get('/personal/{idPersonal}', tags=['personals'], status_code=200)
def get_personal(idPersonal: int = Path(..., title='The ID of the personal')):
    db = Session()
    result = PersonalService(db).get_personal(idPersonal)
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@personal_router.post('/personal', tags=['personals'], status_code=201)
def create_personal(personal: Personal):
    db = Session()
    result = PersonalService(db).create_personal(personal)
    return JSONResponse(status_code=201, content=jsonable_encoder(result))


@personal_router.put('/personal/{idPersonal}', tags=['personals'], status_code=200)
def update_personal(idPersonal: int, personal: Personal):
    db = Session()
    result = PersonalService(db).get_personal(idPersonal)
    if not result:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'message': 'Personal not found'})
    
    print(f'{personal}')
    PersonalService(db).update_personal(idPersonal, personal)
    return JSONResponse(status_code=status.HTTP_200_OK, content={'message': 'Personal updated'})
    