from typing import Optional
from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship


class TransaccionBase(SQLModel):
    cantidad: int = Field(default=None)
    vr_unitario: float = Field(default=None)
    descripcion: str = Field(default=None)


class TransaccionCrear(TransaccionBase):
    pass


class Transaccion(TransaccionBase, table=True):
    id: int | None = Field(primary_key=True)
    factura_id: int | None = Field(foreign_key="factura.id")
    # Relacion virtual no en BD, obtener datos
    transaccion_fac: Optional["Factura"] = Relationship(back_populates="factura_tra")
