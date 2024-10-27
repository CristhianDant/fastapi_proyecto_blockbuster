from config.database import Base
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

class Personal(BaseModel):
    idPersonal: Optional[int] = Field(None)
    nombre: str = Field(min_length=4 , max_length=50)
    direcion: str = Field(min_length=4 , max_length=200)
    telefono: str = Field(min_length=9 , max_length=9)
    fecha_registro: Optional[str] = Field(None)
    email: str = Field(min_length=4 , max_length=100)
    password: str = Field(min_length=4 , max_length=100)

    class Config:
        orm_mode = True
        json_schema_extra = {
            "example": {
                "nombre": "Juan",
                "direcion": "Calle 123",
                "telefono": "123456789",
                "email": "Juan@example.com",
                "password": "123456789",
            }
        }

# class Personal_get(Base):
#     __tablename__ = 'Personal'
#     __table_args__ = {'extend_existing': True}
#     idPersonal = Column(Integer)
#     nombre = Column(String(50))
#     direcion = Column(String(200))
#     telefono = Column(String(9))
#     fecha_registro = Column(DateTime)
#     email = Column(String(100))