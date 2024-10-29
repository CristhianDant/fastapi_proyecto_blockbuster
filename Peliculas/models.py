from config.database import Base
from sqlalchemy import Column, Integer, String , DateTime , Float
from pydantic import BaseModel , Field
from typing import Optional
from datetime import datetime


class Peliculas_database(Base):
    __tablename__ = 'Peliculas'
    
    idPelicula = Column(Integer, primary_key=True, index=True, autoincrement=True)
    titulo = Column(String(50))
    reseña = Column(String(200))
    fecha_estreno = Column(DateTime)
    cantidad = Column(Integer)
    rankin = Column(Float)
    costo = Column(Float)

    # def __str__(self):
    #     text = f'''
    #     TIPO: {type(self)}
    #     Titulo: {self.titulo}
    #     Reseña: {self.reseña}
    #     Fecha de estreno: {self.fecha_estreno}
    #     Cantidad: {self.cantidad}
    #     Rankin: {self.rankin}
    #     '''

    

class Peliculas(BaseModel):
    idPelicula: Optional[int] = Field(None)
    titulo : str = Field(min_length=4 , max_length=50)
    reseña : str = Field(min_length=4 , max_length=200)
    fecha_estreno : datetime
    cantidad : int 
    rankin : float
    costo : float


    class Config:
        orm_mode = True
        json_schema_extra = {
            "example": {
                "titulo": "La vida es bella",
                "reseña": "La vida de un hombre que vive en un campo de concentracion",
                "fecha_estreno": "1997-12-20",
                "cantidad": 10,
                "rankin": 4.5,
                "costo": 10.5
            }
        }
