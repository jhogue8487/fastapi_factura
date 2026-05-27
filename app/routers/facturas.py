from fastapi import APIRouter, HTTPException, status
from datetime import datetime

from sqlmodel import select

from ..modelos.facturas import Factura, FacturaCrear, FacturaEditar
from ..modelos.transacciones import Transaccion
from ..modelos.clientes import Cliente
from ..listas import lista_facturas, lista_clientes

from ..conexion_bd import Sesion_dependencia

ruta_facturas = APIRouter()


@ruta_facturas.get("/facturas", response_model=list[Factura], tags=["Facturas"])
async def listar_facturas(sesion: Sesion_dependencia):
    consulta = select(Factura)
    lista_facturas = sesion.exec(consulta).all()
    return lista_facturas


@ruta_facturas.post("/facturas/{cliente_id}", response_model=Factura, tags=["Facturas"])
async def crear_fatura(
    cliente_id: int, datos_factura: FacturaCrear, sesion: Sesion_dependencia
):
    # buscar cliente en la lista de memoria
    # cliente_encontrado = [c for c in lista_clientes if c.id == cliente_id]
    # cliente_encontrado = None
    # for c in lista_clientes:
    #     if c.id == cliente_id:
    #         cliente_encontrado = c
    #         break
    # BD - validar datos de la factura de json a dict
    datos_factura_val = Factura.model_validate(
        datos_factura.model_dump
    )  # validando datos
    # buscar en la BD cliente
    cliente_encontrado = sesion.get(Cliente, datos_factura_val.get("cliente_id"))
    print("linea 40 antes de if not", cliente_encontrado.__dict__)
    # si no se encuentra el cliente, primer ejemplo error sin status(codigos)
    if not cliente_encontrado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Error: no se encuentra el cliente con id {cliente_id}, debes agregar el cliente.",
        )

    # crear factura
    # validar datos factura - y con BD se valida antes par utilizar esa variable.
    # factura_val = Factura.model_validate(datos_factura.model_dump())
    # factura_val.cliente = cliente_encontrado
    # factura_val.fecha = datetime.now()
    # factura_val.id = len(lista_facturas) + 1
    # # factura_val.transacciones = []
    # lista_facturas.append(factura_val)
    # crear factura ingresando datos a la BD

    sesion.add(datos_factura_val)
    sesion.commit()
    sesion.refresh()
    return datos_factura_val
