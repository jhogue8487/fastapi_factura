from pydantic import BaseModel

class Cliente(BaseModel):
    id: int
    nombre: str
    descripcion: str | None
    email: str
    edad: int