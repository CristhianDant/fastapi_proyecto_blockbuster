from config.database import Base
from sqlalchemy.orm import relationship
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

    cliente = relationship("Cliente_database", back_populates="rentas")
    personal = relationship("Personal_database", back_populates="rentas")


class Renta_encabezado(BaseModel):
    idRenta_enc: Optional[int] = Field(None)
    fecha_inicio: datetime = Field(None)
    fecha_fin: Optional[datetime] = Field(None)
    fin_renta: Optional[bool] = Field(None)
    idPersonal: int 
    idCliente: int
    total: Optional[float] = Field(None)
    subtotal: Optional[float] = Field(None)
    iva: Optional[float] = Field(None)

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "idPersonal": 1,
                "idCliente": 1
            }
        }


class Renta_detalle_database(Base):
    __tablename__ = 'Renta_detalle'
    
    idRenta_det = Column(Integer, primary_key=True, index=True, autoincrement=True)
    idRenta_enc = Column(Integer, ForeignKey('Renta_encabezado.idRenta_enc'))
    idPelicula = Column(Integer, ForeignKey('Peliculas.idPelicula'))
    cantidad = Column(Integer)
    precio = Column(Float)
    pelicula = relationship("Peliculas_database")


class Renta_detalle(BaseModel):
    idRenta_det: Optional[int] = Field(None)
    idRenta_enc: Optional[int] = Field(None)
    idPelicula: int = Field(gt=0)
    cantidad: int = Field(gt=0)
    precio: Optional[float] = Field(None)

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "idPelicula": 1,
                "cantidad": 2
            }
        }