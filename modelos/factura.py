from pydantic import BaseModel, computed_field
from modelos.cliente import Cliente
from .transaccion import Transaccion


class FacturaBase(BaseModel):
    cliente: Cliente
    fecha: str
    transacciones: list[Transaccion]
    # valor_ total: propiedad virtual por los decoradores del metodo del calculo.

    @computed_field
    @property
    def valor_total(self) -> float:
        return sum(transaccion.cantidad for transaccion in self.transacciones)
        # for transaccion in self.transacciones:
        #     return sum(transaccion.vr_unitario * transaccion.cantidad)

    def listar_transacciones():
        # listar tranasacciones que pertenecen a la factura
        pass


class FacturaCrear(FacturaBase):
    pass


class FacturaEditar(FacturaBase):
    pass


class Factura(FacturaBase):
    id: int | None = None
