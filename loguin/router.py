from fastapi import APIRouter, HTTPException
import bcrypt


from middlewares.JWT_bearer import JWTBearer
from Personal.servise import PersonalService
from utils.jwt_tocken import create_token 
from .models import User
from config.database import Session
loguin_router = APIRouter() 

@loguin_router.post('/login')
def login(user: User):
    """
    Login a user
    """
    email = user.username
    personal = PersonalService(Session()).get_personals_email(email=email)


    if not personal:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Validate password
    if not bcrypt.checkpw(user.password.encode('utf-8'), personal.password):
        raise HTTPException(status_code=401, detail="Incorrect password")

    return create_token(user.model_dump())