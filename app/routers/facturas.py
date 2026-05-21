from fastapi import APIRouter, HTTPException
from datetime import datetime

from ..modelos.facturas import Factura, FacturaCrear, FacturaEditar
from ..modelos.transacciones import Transaccion
from ..listas import lista_facturas, lista_clientes

ruta_facturas = APIRouter()


@ruta_facturas.get("/facturas", response_model=list[Factura], tags=["Facturas"])
async def listar_facturas():
    return lista_facturas


@ruta_facturas.post("/facturas/{cliente_id}", response_model=Factura, tags=["Facturas"])
async def crear_fatura(cliente_id: int, datos_factura: FacturaCrear):
    # buscar cliente en la lista
    # cliente_encontrado = [c for c in lista_clientes if c.id == cliente_id]
    cliente_encontrado = None
    for c in lista_clientes:
        if c.id == cliente_id:
            cliente_encontrado = c
            break

    # si no se encuentra el cliente, primer ejemplo error sin status(codigos)
    if not cliente_encontrado:
        raise HTTPException(
            status_code=400,
            detail=f"Error: no se encuentra el cliente con id {cliente_id}, debes agregar el cliente.",
        )

    # crear factura
    # validar datos factura
    factura_val = Factura.model_validate(datos_factura.model_dump())
    factura_val.cliente = cliente_encontrado
    factura_val.fecha = datetime.now()
    factura_val.id = len(lista_facturas) + 1
    # factura_val.transacciones = []
    lista_facturas.append(factura_val)

    return factura_val
