import uvicorn
from fastapi import FastAPI , status
from fastapi.responses import JSONResponse , RedirectResponse


from config.database import engine , Base


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

from Renta.router import renta_router
app.include_router(renta_router)

from loguin.router import loguin_router
app.include_router(loguin_router)

## Create database tables
Base.metadata.create_all(bind=engine)

@app.get("/" , tags=["Root"])
def read_root():
    """
    Este endpoint redirige a la documentación de la API
    """
    return RedirectResponse(url="/docs")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5050)



