from datetime import datetime
from .models import Cliente , Cliente_database 
from sqlalchemy import select , text


class ClientService(Cliente_database):
    def __init__(self , db):
        self.db = db

    def get_clientes(self):
        """
        Get all the clients
        """
        sql_query = text("SELECT * FROM Cliente")
        result = self.db.execute(sql_query).fetchall()
        return result
    

    def get_clientes_customer(self):
        list_clientes= []
        # ## Desendente
        # result = self.db.execute(select(Cliente_database).order_by(Cliente_database.idCliente.desc()))
        # ## Ascendente
        # result = self.db.execute(select(Cliente_database).order_by(Cliente_database.idCliente.asc()))
        # clientes = result.scalars().all()

        result = self.db.execute(
            select(Cliente_database.idCliente,
                Cliente_database.nombre,
                Cliente_database.direcion,
                Cliente_database.telefono,
                Cliente_database.fecha_registro)
        )
        
        
        for cliente in result:
            list_clientes.append({
                "idCliente": cliente.idCliente,
                "nombre": cliente.nombre,
                "direcion": cliente.direcion,
                "telefono": cliente.telefono,
                "fecha_registro": cliente.fecha_registro
            })

        return list_clientes
    
    def get_cliente(self, idCliente):
        """
        Get a client by id
        """
        result = self.db.query(Cliente_database).filter(Cliente_database.idCliente == idCliente).first()
        return result   
    
    def get_cliente_by_name(self, nombre):
        """
        Get a client by name
        """
        result = self.db.query(Cliente_database).filter(Cliente_database.nombre == nombre).first()
        return result


    def create_cliente(self, cliente: Cliente):
        """
        Create a new client
        """
        cliente_data = cliente.model_dump()

        ## Valores por defecto
        cliente_data['fecha_registro'] = datetime.now()


        new_cliente = Cliente_database(**cliente_data)
        self.db.add(new_cliente)
        self.db.commit()
        self.db.refresh(new_cliente)
        return new_cliente

    def update_cliente(self, idCliente, cliente: Cliente):
        """
        Update a client
        """
        # Valores que no se deben actualizar
        list_exclude_fields = ['idCliente' , 'fecha_registro']

        client = self.get_cliente(idCliente)

        for key, value in cliente.model_dump().items():
            if key not in list_exclude_fields:
                setattr(client, key, value)
                
        self.db.commit()
        self.db.refresh(client)
        return client
    
    def delete_cliente(self, idCliente):
        """
        Delete a client
        """
        client = self.get_cliente(idCliente)
        self.db.delete(client)
        self.db.commit()
        return client
    
