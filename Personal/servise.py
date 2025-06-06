import bcrypt
from datetime import datetime

from .models import Personal , Personal_database 

from sqlalchemy import select , text

class PersonalService(Personal_database):
    def __init__(self , db):
        self.db = db

    def get_personals_deprecate(self):
        """
        Get all the personals
        """
        result = self.db.query(Personal_database).all()
        return result
    
    def get_personals_email(self, email):
        """
        Get all the personals
        """
        result = self.db.query(Personal_database).filter(Personal_database.email == email).first()
        
        if not result:
            return None
        
        
        return result

    


    def get_personals(self):
        """
        Get all the personals
        """

        result = self.db.execute(text('''
        SELECT
            idPersonal,
            nombre,
            direcion,
            telefono,
            fecha_registro,
            email
        FROM
            Personal
        ''')).mappings().all()

        return result

    def get_personal(self, idPersonal):
        """
        Get a personal by id
        """

        result = self.db.execute(text('''
        SELECT
            idPersonal,
            nombre,
            direcion,
            telefono,
            fecha_registro,
            email
        FROM
            Personal
        WHERE
            idPersonal = :idPersonal
        '''), {'idPersonal': idPersonal}).mappings().first()

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
    
    def update_password(self, data : dict):
        """
        Update password 
        DATA {
            idPersonal: int
            password_legaci: str
            new_password: str
        }
        """
        print(f'estamo en el servicio')
        ## BUSCAR EL USUARIO
        personal = self.get_personal(data['idPersonal'])
        ## ESTRAER EL PASSWORD
        password = personal.password
        ## VALIDAR EL PASSWORD
        
        #import pdb; pdb.set_trace()

        if bcrypt.checkpw(data['password_legaci'].encode('utf-8'), password.encode('utf-8')):
            ## HASHEAR EL NUEVO PASSWORD
            hashed_password = bcrypt.hashpw(data['new_password'].encode('utf-8'), bcrypt.gensalt())
            ## ACTUALIZAR EL PASSWORD
            personal.password = hashed_password
            self.db.commit()
            self.db.refresh(personal)
            return personal
        else:
            return None
    def update_personal(self, idPersonal, personal: Personal):
        """
        Update a personal
        """
        # Valores que no se deben actualizar
        list_exclude_fields = ['idPersonal', 'fecha_registro' , 'password']

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