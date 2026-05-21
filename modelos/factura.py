from pydantic import BaseModel, computed_field
from modelos.cliente import Cliente
from .transaccion import Transaccion


class FacturaBase(BaseModel):
    cliente: Cliente
    fecha: str
    transacciones: list[Transaccion] = []
    # valor_ total: propiedad virtual por los decoradores del metodo del calculo.

    @computed_field
    @property
    def valor_total(self) -> float:
        return sum(transaccion.cantidad for transaccion in self.transacciones)
        # for transaccion in self.transacciones:
        #     return sum(transaccion.vr_unitario * transaccion.cantidad)

    @computed_field
    @property
    def listar_transacciones(self) -> list[Transaccion]:
        # listar tranasacciones que pertenecen a la factura
        transacciones_factura = []
        factura_id_actual = getattr(self, "id", None)
        if factura_id_actual is None:
            return transacciones_factura

        # return [t for t in self.transacciones if t.id == factura_id_actual]
        for t in self.transacciones:
            if t.factura_id == factura_id_actual:
                transacciones_factura = self.transacciones
                break
        return transacciones_factura


class FacturaCrear(FacturaBase):
    pass


class FacturaEditar(FacturaBase):
    pass


class Factura(FacturaBase):
    id: int | None = None
