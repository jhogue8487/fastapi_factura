from pydantic import BaseModel

class ClienteBase(BaseModel):
    nombre: str
    descripcion: str | None
    email: str
    edad: int

class ClienteCrear(ClienteBase):
    pass

class ClienteEditar(ClienteBase):
    pass

class Cliente(ClienteBase):
    id: int | None = None
