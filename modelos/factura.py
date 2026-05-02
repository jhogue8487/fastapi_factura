from pydantic import BaseModel
from cliente import Cliente
from transaccion import Transaccion

class Factura(BaseModel):
    id: int
    cliente: Cliente
    transacciones: list[Transaccion]