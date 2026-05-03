from pydantic import BaseModel

class Transaccion(BaseModel):
    id: int
    cantidad: int
    descripcion: str
