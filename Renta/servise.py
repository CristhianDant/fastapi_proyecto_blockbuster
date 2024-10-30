from .models import Renta_encabezado , Renta_encabezado_database , Renta_detalle , Renta_detalle_database , datetime


from Peliculas.servise import PeliculasService
from Personal.servise import PersonalService
from Cliente.servise import ClientService

class RentaServise:

    def __init__(self , db):
        self.db = db

    def get_rentas(self):
        """
        Get all the rentas
        """
        result = self.db.query(Renta_encabezado_database).order_by(Renta_encabezado_database.idRenta_enc.desc()).limit(30).all()

        return result
    
    def get_renta(self, idRenta_enc):
        """
        Get a renta by id
        """
        renta_enc = self.db.query(Renta_encabezado_database).filter(Renta_encabezado_database.idRenta_enc == idRenta_enc).first()
        renta_det = self.db.query(Renta_detalle_database).filter(Renta_detalle_database.idRenta_enc == idRenta_enc).all()

        renta = {
            "renta_enc": renta_enc,
            "detalle": renta_det
        }

        return renta


    def _reguister_renta_det(self, idRenta_enc, detalle):
        """
        Reguister the renta detail
        """
        total = 0 

        # Crear el detalle de la renta
        for item in detalle:
            renta_det_data = item.model_dump()
            
            renta_det_data['idRenta_enc'] = idRenta_enc
            pelicula = PeliculasService(self.db).get_pelicula(renta_det_data['idPelicula'])
            if not pelicula:
                raise ValueError("Pelicula no encontrada")
            renta_det_data['precio'] = pelicula.precio
            new_renta_det = Renta_detalle_database(**renta_det_data)
            total += renta_det_data['cantidad'] * renta_det_data['precio']
            PeliculasService(self.db).disminuir_cantidad(idPelicula=renta_det_data['idPelicula'], cantidad=renta_det_data['cantidad'])
            self.db.add(new_renta_det)

        return total

    def create_renta(self, renta_enc : Renta_encabezado , detalle : list[Renta_detalle]):
        """
        Create a new renta
        """

        renta_enc_data = renta_enc.model_dump()

        total = self._reguister_renta_det(renta_enc.idRenta_enc, detalle)
        # Valores por defecto
        renta_enc_data['fecha_inicio'] = datetime.now()
        renta_enc_data['fin_renta'] 
        renta_enc_data['total'] = total
        renta_enc_data['iva'] = total * 0.18
        renta_enc_data['subtotal'] = total - renta_enc_data['iva']
        

        # Crear el encabezado en la renta 
        new_renta_enc = Renta_encabezado_database(**renta_enc_data)

        self.db.add(new_renta_enc)
        self.db.commit()
        self.db.refresh(new_renta_enc)


        return renta_enc.idRenta_enc
    

    def update_renta(self, idRenta_enc, renta_enc : Renta_encabezado , detalle : list[Renta_detalle]):
        """
        Update a renta
        """

        # Eliminar el detalle de la renta
        self.db.query(Renta_detalle_database).filter(Renta_detalle_database.idRenta_enc == idRenta_enc).delete()

        total = self._reguister_renta_det(idRenta_enc, detalle)

        # Actualizar el encabezado de la renta
        renta_enc_data = renta_enc.model_dump()
        renta_enc_data['total'] = total
        renta_enc_data['iva'] = total * 0.18
        renta_enc_data['subtotal'] = total - renta_enc_data['iva']

        list_exclude = ['idRenta_enc' , 'fecha_inicio' , 'fecha_fin' , 'fin_renta']

        renta_enc = self.get_renta(idRenta_enc)['renta_enc']

        for key in renta_enc_data:
            if key not in list_exclude:
                setattr(renta_enc, key, renta_enc_data[key])

        self.db.commit()
        self.db.refresh(renta_enc)
        return renta_enc.idRenta_enc
    

    def delete_renta(self, idRenta_enc):
        """
        Delete a renta
        """

        renta_enc = self.db.query(Renta_encabezado_database).filter(Renta_encabezado_database.idRenta_enc == idRenta_enc).first()

        if not renta_enc['fin_renta']:
            raise ValueError("No se puede eliminar una renta que no ha finalizado")
        
        self.db.query(Renta_detalle_database).filter(Renta_detalle_database.idRenta_enc == idRenta_enc).delete()
        self.db.query(Renta_encabezado_database).filter(Renta_encabezado_database.idRenta_enc == idRenta_enc).delete()

        self.db.commit()

        return renta_enc.idRenta_enc
    
    def finalizar_renta(self, idRenta_enc):
        """
        Finalizar una renta
        """
        
        renta_enc = self.db.query(Renta_encabezado_database).filter(Renta_encabezado_database.idRenta_enc == idRenta_enc).first()

        if renta_enc['fin_renta']:
            raise ValueError("La renta ya ha sido finalizada")

        renta_enc['fin_renta'] = True
        renta_enc['fecha_fin'] = datetime.now()

        self.db.commit()
        self.db.refresh(renta_enc)
        return renta_enc.idRenta_enc
    

    def get_ulitma_renta(self):
        """
        Get the last renta
        """
        renta = self.db.query(Renta_encabezado_database).order_by(Renta_encabezado_database.idRenta_enc.desc()).first()


        id = renta.idRenta_enc if renta else 0
        return  id + 1 

    
