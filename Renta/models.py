from config.database import Base
from sqlalchemy import Column, Integer, String , Float, DateTime , ForeignKey , Boolean
from pydantic import BaseModel , Field
from typing import Optional
from datetime import datetime



class Renta_encabezado_database(Base):
    __tablename__ = 'Renta_encabezado'
    
    idRenta_enc = Column(Integer, primary_key=True, index=True, autoincrement=True)
    fecha_inicio = Column(DateTime)
    fecha_fin = Column(DateTime)
    fin_renta = Column(Boolean)
    idPersonal = Column(Integer, ForeignKey('Personal.idPersonal'))
    idCliente = Column(Integer, ForeignKey('Cliente.idCliente'))
    total = Column(Float)
    subtotal = Column(Float)
    iva = Column(Float)


class Renta_encabezado(BaseModel):
    idRenta_enc: Optional[int] = Field(None)
    fecha_inicio: datetime = Field(None)
    fecha_fin: Optional[datetime] = Field(None)
    fin_renta: Optional[bool] = Field(None)
    idPersonal: int 
    idCliente: int
    total: float = Field(gt=0)
    subtotal: float = Field(gt=0)
    iva: float = Field(gt=0)

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "fin_renta": False,
                "idPersonal": 1,
                "idCliente": 1,
                "total": 100.0,
                "subtotal": 82.0,
                "iva": 18.0
            }
        }


class Renta_detalle_database(Base):
    __tablename__ = 'Renta_detalle'
    
    idRenta_det = Column(Integer, primary_key=True, index=True, autoincrement=True)
    idRenta_enc = Column(Integer, ForeignKey('Renta_encabezado.idRenta_enc'))
    idPelicula = Column(Integer, ForeignKey('Peliculas.idPelicula'))
    cantidad = Column(Integer)
    precio = Column(Float)


class Renta_detalle(BaseModel):
    idRenta_det: Optional[int] = Field(None)
    idRenta_enc: int
    idPelicula: int
    cantidad: int = Field(gt=0)
    precio: float = Field(gt=0)

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "idRenta_enc": 1,
                "idPelicula": 1,
                "cantidad": 2,
                "precio": 50.0
            }
        }