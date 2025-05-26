from sqlalchemy import select

from .models import Renta_encabezado , Renta_encabezado_database , Renta_detalle , Renta_detalle_database , datetime
from Peliculas.servise import Peliculas_database , PeliculasService
from Personal.servise import Personal_database
from Cliente.servise import Cliente_database

class RentaServise:

    def __init__(self , db):
        self.db = db

    def get_rentas(self):
        """
        Get all the rentas
        """
        result = self.db.execute(
            select(
                Renta_encabezado_database.idRenta_enc,
                Renta_encabezado_database.fecha_inicio,
                Renta_encabezado_database.fecha_fin,
                Renta_encabezado_database.fin_renta,
                Renta_encabezado_database.total,
                Renta_encabezado_database.iva,
                Renta_encabezado_database.subtotal,
                Renta_encabezado_database.idCliente,
                Cliente_database.nombre.label("cliente"),
                Renta_encabezado_database.idPersonal,
                Personal_database.nombre.label("personal")
            ).join(
                Cliente_database , Renta_encabezado_database.idCliente == Cliente_database.idCliente
            ).join(
                Personal_database , Renta_encabezado_database.idPersonal == Personal_database.idPersonal
            )
        ).mappings().all()

        return result
    
    def get_list_rentas_between_dates(self , fecha_inicio , fecha_fin):
        """
        Get all the rentas between two dates
        """
        stmt = select(
            Renta_encabezado_database.idRenta_enc,
            Renta_encabezado_database.fecha_inicio,
            Renta_encabezado_database.fecha_fin,
            Renta_encabezado_database.fin_renta,
            Renta_encabezado_database.total,
            Renta_encabezado_database.iva,
            Renta_encabezado_database.subtotal,
            Renta_encabezado_database.idCliente,
            Cliente_database.nombre.label("cliente"),
            Renta_encabezado_database.idPersonal,
            Personal_database.nombre.label("personal")
        ).join(
            Cliente_database , Renta_encabezado_database.idCliente == Cliente_database.idCliente
        ).join(
            Personal_database , Renta_encabezado_database.idPersonal == Personal_database.idPersonal
        ).where(
            Renta_encabezado_database.fecha_inicio >= fecha_inicio
        ).where(
            Renta_encabezado_database.fecha_inicio <= fecha_fin
        )

        result = self.db.execute(stmt).mappings().all()
        
        return result

    
    def get_renta(self, idRenta_enc):
        """
        Get a renta by id
        """
        #renta_enc = self.db.query(Renta_encabezado_database).filter(Renta_encabezado_database.idRenta_enc == idRenta_enc).first()
        renta_enc = self.db.execute(
            select(
                Renta_encabezado_database.idRenta_enc,
                Renta_encabezado_database.fecha_inicio,
                Renta_encabezado_database.fecha_fin,
                Renta_encabezado_database.fin_renta,
                Renta_encabezado_database.total,
                Renta_encabezado_database.iva,
                Renta_encabezado_database.subtotal,
                Renta_encabezado_database.idCliente,
                Cliente_database.nombre.label("cliente"),
                Renta_encabezado_database.idPersonal,
                Personal_database.nombre.label("personal")
            ).join(
                Cliente_database , Renta_encabezado_database.idCliente == Cliente_database.idCliente
            ).join(
                Personal_database , Renta_encabezado_database.idPersonal == Personal_database.idPersonal
            ).where(Renta_encabezado_database.idRenta_enc == idRenta_enc)
        ).mappings().first()

    
        renta_det = self.db.execute(
            select(
                Renta_detalle_database.idRenta_det,
                Renta_detalle_database.idRenta_enc,
                Renta_detalle_database.idPelicula,
                Renta_detalle_database.cantidad,
                Renta_detalle_database.precio,
                Peliculas_database.titulo.label("pelicula")
            ).join(Peliculas_database , Renta_detalle_database.idPelicula == Peliculas_database.idPelicula)
            .where(Renta_detalle_database.idRenta_enc == idRenta_enc)
        ).mappings().all()

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

            renta_det_data['precio'] = pelicula.costo
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

        id = self.get_ulitma_renta()

        total = self._reguister_renta_det(id , detalle)
        # Valores por defecto
        renta_enc_data['fecha_inicio'] = datetime.now()
        renta_enc_data['fin_renta'] = ""
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


        if renta_enc is None:
            raise ValueError("La renta no existe")

        if renta_enc.fin_renta:
            raise ValueError("La renta ya ha sido finalizada")
        
        renta_det = self.db.query(Renta_detalle_database).filter(Renta_detalle_database.idRenta_enc == idRenta_enc).all()

        for det in renta_det:
            pelicula = PeliculasService(self.db).get_pelicula(det.idPelicula)
            if pelicula:
                PeliculasService(self.db).aumentar_cantidad(pelicula.idPelicula, det.cantidad)

        renta_enc.fin_renta = True
        renta_enc.fecha_fin = datetime.now()

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

    
