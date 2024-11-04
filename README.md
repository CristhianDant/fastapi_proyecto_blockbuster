# My Api BlockBuster

Mi Api BlockBuster es una aplicación basada en FastAPI diseñada para gestionar una tienda de alquiler de videos. Este proyecto incluye funcionalidades para la gestión de clientes, películas, alquileres y personal.
## Instalacion 

1. Clonar Repositorio
``` bash
git clone https://github.com/yourusername/my-api-blockbuster.git
cd my-api-blockbuster
```

2. Crear el entorno virtual 
``` bash
python -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`
```

3. Install dependecias 

``` bash
pip install -r requirements.txt
```

4. Crearcion de **.env** 

``` bash
SECRET_KEY='TU_KEY'
```

## API Endpoints 


### Cliente
- **GET /clientes**: Get all clients.
- **GET /clientes/{idCliente}**: Get a client by ID.
- **GET /clientes/**: Get a client by name.
- **POST /clientes**: Create a new client.
- **PUT /clientes/{idCliente}**: Update a client.
- **DELETE /clientes/{idCliente}**: Delete a client.

### Peliculas
- **GET /peliculas**: Get all movies.
- **GET /peliculas/{idPelicula}**: Get a movie by ID.
- **POST /peliculas**: Create a new movie.
- **PUT /peliculas/{idPelicula}**: Update a movie.
- **DELETE /peliculas/{idPelicula}**: Delete a movie.

### Renta
- **GET /rentas**: Get all rentals.
- **GET /rentas/{idRenta_enc}**: Get a rental by ID.
- **POST /rentas**: Create a new rental.
- **PUT /rentas/{idRenta_enc}**: Update a rental.
- **DELETE /rentas/{idRenta_enc}**: Delete a rental.
- **POST /rentas/finalizar/{idRenta_enc}**: Finalize a rental.

### Personal
- **POST /personal**: Create a new personal staff member.

### Loguin
- **POST /loguin**: Log in a user.


