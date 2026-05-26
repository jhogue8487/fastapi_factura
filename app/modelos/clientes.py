from typing import TYPE_CHECKING

from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .facturas import Factura


class ClienteBase(SQLModel):
    nombre: str = Field(default=None)
    descripcion: str | None = Field(default=None)
    email: str = Field(default=None)
    edad: int = Field(default=None)


class ClienteCrear(ClienteBase):
    pass


class ClienteEditar(ClienteBase):
    pass


class Cliente(ClienteBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    # Relacion virtual, no en BD, obtener datos
    facturas: list["Factura"] = Relationship(
        back_populates="cliente"
    )  # esta variable con modelo factura y viceversa
