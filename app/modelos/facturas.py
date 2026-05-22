from pydantic import BaseModel, computed_field
from app.modelos.clientes import Cliente
from .transacciones import Transaccion


class FacturaBase(BaseModel):
    cliente: Cliente
    fecha: str
    transacciones: list[Transaccion] = []
    # valor_ total: propiedad virtual por los decoradores del metodo del calculo.

    @computed_field
    @property
    def valor_total(self) -> float:
        # consultar id actual para poder filtrar
        factura_id_actual = getattr(self, "id", None)
        if factura_id_actual is None or not self.transacciones:
            return 0.0
        return sum(
            t.cantidad * t.vr_unitario
            for t in self.transacciones
            if t.factura_id == factura_id_actual
        )
        # for t in self.transacciones:
        #     if t.factura_id == factura_id_actual:
        #         return sum(t.cantidad * t.vr_unitario)


class FacturaCrear(FacturaBase):
    pass


class FacturaEditar(FacturaBase):
    pass


class Factura(FacturaBase):
    id: int | None = None
