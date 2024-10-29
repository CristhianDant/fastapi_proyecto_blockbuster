from .models import Peliculas , Peliculas_database

class PeliculasService(Peliculas_database):
    def __init__(self , db):
        self.db = db

    def get_peliculas(self):
        result = self.db.query(Peliculas_database).all()   
        return result
    
    def get_pelicula(self , idPelicula):
        result = self.db.query(Peliculas_database).filter(Peliculas_database.idPelicula == idPelicula).first()
        return result
    
    def create_pelicula(self , pelicula: Peliculas):
        pelicula_data = pelicula.model_dump()
        new_pelicula = Peliculas_database(**pelicula_data)
        self.db.add(new_pelicula)
        self.db.commit()
        self.db.refresh(new_pelicula)
        return new_pelicula
    

    def update_pelicula(self , idPelicula , pelicula: Peliculas):

        ## Get the pelicula
        get_pelicula = self.db.query(Peliculas_database).filter(Peliculas_database.idPelicula == idPelicula).first()

        print(get_pelicula)
        list_exlude_fields = ['idPelicula', 'cantidad']
        ## Update the pelicula
        for key , value in pelicula.model_dump().items():
            if key not in list_exlude_fields:
                setattr(get_pelicula , key , value)

        self.db.commit()
        self.db.refresh(get_pelicula)
        return get_pelicula
    

    def aumentar_cantidad(self , idPelicula , cantidad):
        
        ## Get the pelicula
        get_pelicula = self.db.query(Peliculas_database).filter(Peliculas_database.idPelicula == idPelicula).first()
        get_pelicula.cantidad += cantidad
        self.db.commit()
        self.db.refresh(get_pelicula)
        return get_pelicula
    
    def disminuir_cantidad(self , idPelicula , cantidad):
            
            ## Get the pelicula
            get_pelicula = self.db.query(Peliculas_database).filter(Peliculas_database.idPelicula == idPelicula).first()
            get_pelicula.cantidad -= cantidad
            if get_pelicula.cantidad < 0:
                raise ValueError('No hay suficientes peliculas')
            self.db.commit()
            self.db.refresh(get_pelicula)
            return get_pelicula
    
    def delete_pelicula(self , idPelicula):
        ## Get the pelicula
        get_pelicula = self.db.query(Peliculas_database).filter(Peliculas_database.idPelicula == idPelicula).first()
        self.db.delete(get_pelicula)
        self.db.commit()
        return idPelicula