from fastapi import FastAPI , status
from fastapi.responses import JSONResponse

from config.database import engine , Base

### SHELL COMMANDS
# uvicorn main:app --reload --port 5050

app = FastAPI()
app.title = "My Api BlockBuster"
app.version = "0.0.1"

## add_middleware
from middlewares.Error_handler import ErrorHandler
app.add_middleware(ErrorHandler)

## Import routers
from Cliente.router import cliente_router
app.include_router(cliente_router)

from Personal.router import personal_router
app.include_router(personal_router)

from Peliculas.router import peliculas_router
app.include_router(peliculas_router)

## Create database tables
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    """
    Endpoint de bienvenida 
    """
    return JSONResponse(
        content={"message": "Hello World"},
        status_code=status.HTTP_200_OK
    )

