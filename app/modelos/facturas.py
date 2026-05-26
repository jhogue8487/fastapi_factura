from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, computed_field
from sqlmodel import Relationship, SQLModel, Field

# solo para no mostrar advertencias de pylance en nuestro codigo.
if TYPE_CHECKING:
    from .clientes import Cliente
    from .transacciones import Transaccion


class FacturaBase(SQLModel):
    # cliente: Cliente#pasa como llave foranea
    fecha: str = Field(default=None)
    # transacciones: list[Transaccion] = []#pasa como llave foranea, en el modelo transacciones

    @computed_field
    @property
    def valor_total(self) -> float:
        # # consultar id actual para poder filtrar cuando guardamos en memoria.
        # con bd sqlmodel realiza el filtro
        factura_id_actual = getattr(self, "id", None)
        if factura_id_actual is None or not self.transacciones:
            return 0.0
        return sum(t.cantidad * t.vr_unitario for t in self.transacciones)


class FacturaCrear(FacturaBase):
    pass


class FacturaEditar(FacturaBase):
    pass


class Factura(FacturaBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    cliente_id: int = Field(foreign_key="cliente.id")
    # Relacion virtual no en BD, obtener datos
    factura_cli: Optional["Cliente"] = Relationship(
        back_populates="cliente_fac"
    )  # esta variable con modelo cliente y viceversa.
    factura_tra: list["Transaccion"] = Relationship(back_populates="transaccion_fac")
