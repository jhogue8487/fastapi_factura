from pydantic import BaseModel

class Transaccion(BaseModel):
    id: int
    cantidad: int
    vr_unitario: float
    descripcion: str
