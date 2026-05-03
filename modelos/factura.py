from pydantic import BaseModel
from modelos.cliente import Cliente
from .transaccion import Transaccion

class Factura(BaseModel):
    id: int
    cliente: Cliente
    transacciones: list[Transaccion]

#Ahora que ya leíste todos los archivos, termina de conectar los puntoss.
#Factura.model_rebuild()