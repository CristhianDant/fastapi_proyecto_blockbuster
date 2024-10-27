import bcrypt
from datetime import datetime

from .models import Personal , Personal_database 

class PersonalService(Personal_database):
    def __init__(self , db):
        self.db = db

    def get_personals(self):
        """
        Get all the personals
        """
        result = self.db.query(Personal_database).all()

        for personal in result:
            personal.password = '********'
        return result

    def get_personal(self, idPersonal):
        """
        Get a personal by id
        """
        result = self.db.query(Personal_database).filter(Personal_database.idPersonal == idPersonal).first()
        if result:
            result.password = '********'
        return result
    
    def create_personal(self, personal: Personal):
        """
        Create a new personal
        """
        personal_data = personal.model_dump()

        # Hash password
        hashed_password = bcrypt.hashpw(personal_data['password'].encode('utf-8'), bcrypt.gensalt())
        personal_data['password'] = hashed_password
        # Valores por defecto
        personal_data['fecha_registro'] = datetime.now()

        new_personal = Personal_database(**personal_data)
        self.db.add(new_personal)
        self.db.commit()
        self.db.refresh(new_personal)
        return new_personal
    
    def update_personal(self, idPersonal, personal: Personal):
        """
        Update a personal
        """
        # Valores que no se deben actualizar
        list_exclude_fields = ['idPersonal', 'fecha_registro']

        personal_update = self.get_personal(idPersonal)

        for key, value in personal.model_dump().items():
            if key not in list_exclude_fields:
                setattr(personal_update, key, value)
                
        self.db.commit()
        self.db.refresh(personal_update)
        return personal
    
    def delete_personal(self, idPersonal):
        """
        Delete a personal
        """
        personal = self.get_personal(idPersonal)
        self.db.delete(personal)
        self.db.commit()
        return personal