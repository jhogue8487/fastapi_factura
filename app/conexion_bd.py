from sqlmodel import Session, create_engine
from typing import Annotated
from fastapi import Depends

# nombre de la base de datos
sqlite_nombre = "bd_clientes.sqlite3"
# conexion a la base de datos sqlite
sqlite_url = f"sqlite:///{sqlite_nombre}"

# motor de base de datos que utilizaremos
motor_bd = create_engine(sqlite_url)


# obtener una sesion en la base de datos
def get_session():
    with Session as mi_sesion:
        yield mi_sesion  # para retornar, o entregar la sesion. Utilizarla en nuestos modelos con Annotated


# definir la dependencia y registra mi sesion como dependencia
Sesion_dependencia = Annotated[Session, Depends(get_session)]
