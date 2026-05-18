from pydantic import BaseModel
from modelos.cliente import Cliente
from .transaccion import Transaccion

class FacturaBase(BaseModel):
    cliente: Cliente
    fecha: str
    transacciones: list[Transaccion]
    total: float

    @property
    def cantidad_total(self):
        #return sum(transaccion.cantidad for transaccion in self.transacciones)
        for transaccion in self.transacciones:
            return sum(transaccion.vr_unitario*transaccion.cantidad)
        
class FacturaCrear(FacturaBase):
    pass

class FacturaEditar(FacturaBase):
    pass

class Factura(FacturaBase):
    id: int | None = None