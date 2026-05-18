from pydantic import BaseModel

class TransaccionBase(BaseModel):
    cantidad: int
    vr_unitario: float
    descripcion: str

class TransaccionCrear(TransaccionBase):
    pass

class Transaccion(TransaccionBase):
    id : int | None = None
