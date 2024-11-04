from config.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String , DateTime  
from pydantic import BaseModel , Field
from typing import Optional

class Personal_database(Base):
    __tablename__ = 'Personal'
    
    idPersonal = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(50))
    direcion = Column(String(200))
    telefono = Column(String(9))
    fecha_registro = Column(DateTime)
    email = Column(String(100))
    password = Column(String(100))

    rentas = relationship("Renta_encabezado_database", back_populates="personal")


class Personal(BaseModel):
    idPersonal: Optional[int] = Field(None)
    nombre: str = Field(min_length=4 , max_length=50)
    direcion: str = Field(min_length=4 , max_length=200)
    telefono: str = Field(min_length=9 , max_length=9)
    fecha_registro: Optional[str] = Field(None)
    email: str = Field(min_length=4 , max_length=100)
    password: str = Field(min_length=4 , max_length=100)

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "nombre": "Juan",
                "direcion": "Calle 123",
                "telefono": "123456789",
                "email": "Juan@example.com",
                "password": "123456789",
            }
        }

class UpdatePasswordRequest(BaseModel):
    idPersonal: int = Field(..., example=1)
    password_legaci: str = Field(..., example="old_password123")
    new_password: str = Field(..., example="new_password456")
