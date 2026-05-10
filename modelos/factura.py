from pydantic import BaseModel
from modelos.cliente import Cliente
from .transaccion import Transaccion

class Factura(BaseModel):
    id: int
    cliente: Cliente
    transacciones: list[Transaccion]
    total: int

    @property
    def cantidad_total(self):
        #return sum(transaccion.cantidad for transaccion in self.transacciones)
        for transacciones in self.transacciones:
            return sum(transacciones.cantidad)