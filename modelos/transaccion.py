from pydantic import BaseModel

class Transaccion():
    id: int
    cantidad: int
    descripcion: str
    