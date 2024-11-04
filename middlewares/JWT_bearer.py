
from fastapi import HTTPException , Request
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials


from utils.jwt_tocken import validate_token



class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):

        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        
        
        if data is None:
            raise HTTPException(status_code=403, detail="Invalid token or expired token")

        return data


