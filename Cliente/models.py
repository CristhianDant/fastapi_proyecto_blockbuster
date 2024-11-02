from config.database import Base
from sqlalchemy import Column, Integer, String , DateTime
from sqlalchemy.orm import relationship
from pydantic import BaseModel , Field
from typing import Optional

class Cliente_database (Base):
    __tablename__ = 'Cliente'
    
    idCliente = Column(Integer, primary_key=True, index=True , autoincrement=True)
    nombre = Column(String(50))
    direcion = Column(String(200))
    telefono = Column(String(9))
    fecha_registro = Column(DateTime)

    rentas = relationship("Renta_encabezado_database", back_populates="cliente")



class Cliente(BaseModel):
    idCliente: Optional[int] = Field(None)
    nombre: str = Field(min_length=4 , max_length=50)
    direcion: str = Field(min_length=4 , max_length=200)
    telefono: str = Field(min_length=9 , max_length=9)
    fecha_registro: Optional[str] = Field(None)

    class Config:
        json_schema_extra = {
            "example": {
                "nombre": "Juan",
                "direcion": "Calle 123",
                "telefono": "123456789",
            }
        }
