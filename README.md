Este es un proyecto de aprendizaje de desarrollo de una API, para la formacion SENA.
Se trata de un proyecto de clientes, facturas y transacciones, al iniciar el proyecto se crea utilizando el gestor de dependencias uv, como se puede apreciar en los archivos.

Al inicio del proyecto no tenemos estructura, solo el archivo main, donde realizamos todo el codidgo, y vamos editando y agregando complejidad.

En el archivo main, creamos los 5 endpoint para clientes (listar un cliente y todos los clinentes, crear, editar y eliminar), junto con le modelo de clientes, y todo esto guardando en memoria.

Despues separamos el modelo en una carpeta, y creamos los otros modelos de facturas y transacciones, y que los aprendices realizaran los endpoint correspondientes, para mas adelante revisar y aclarar la creacion de los endpoint y las relaciones entre los modelos(simulando una base de datos).

Al crear una estructura del proyecto, separamos en carpetas nuestros archivos, agregando el enrutador para el manejo de las rutas de nuestros endpoint y poder limpiar nuestro archivo main.

Ahora realizaremos el uso de la base de datos SQLite:

1. Instalar dependencia sqlmodel
2. Crear el archivo _.py, para configuracion:
   Importando las clases session, create_engine
   Definir nombre base de datos _.db ó _.db3 ó _.sqlite ó \*.sqlite3 entre otras
   Crear la URL: sqlite:///nombre_bd
3. Crear el motor ó engine, para gestionar la sesion con get_session
4. Registrar la sesión como dependencia en FastAPI
   Para que FastAPI use la sesión en sus endpoints:
   Importa Depends de FastAPI.
   Define una dependencia que gestione la sesión mediante get_session, facilitando el acceso a la base de datos desde cualquier endpoint.
5. Adaptar los modelos para almacenar datos en bd
   Modificar modelo:
   Si usas modelos de Pydantic, ajústalos para heredar de SQLModel en vez de BaseModel. Esto conecta los modelos con la bd
6. Creación de tablas:
   En el modelo que representa una tabla, añade table=True para que SQLModel cree automáticamente la tabla en la bd.
   Hereda los atributos comunes de un modelo base (sin table=True) para evitar duplicaciones y asegurar que se incluyan todos los campos necesarios.

   Ejemplo de implementación:
   Define un modelo ClienteBase para los datos comunes.
   Crea un modelo Cliente, que herede de ClienteBase y de SQLModel, con table=True para almacenar los registros en la tabla correspondiente.
