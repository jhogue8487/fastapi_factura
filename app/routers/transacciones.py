from fastapi import APIRouter, HTTPException
from datetime import datetime

from ..modelos.transacciones import Transaccion, TransaccionCrear
from ..modelos.facturas import Factura, FacturaCrear
from ..listas import lista_transacciones, lista_clientes, lista_facturas

ruta_transanccciones = APIRouter()


@ruta_transanccciones.get("/transacciones", response_model=list[Transaccion])
async def listar_transacciones():
    return lista_transacciones


@ruta_transanccciones.post("/transacciones/{factura_id}")
async def crear_transaccion(
    factura_id: int, datos_transaccion: TransaccionCrear, cliente_id: int
):
    # Consular si cliente_id existe; para consultar si tiene facturas con ese id y adicionar una transaccion o crear nueva factura.
    # cliente_encontrado = next((c for c in db_clientes if c.id == cliente_id), None)
    cliente_encontrado = None
    for c in lista_clientes:
        if c.id == cliente_id:
            cliente_encontrado = c
            break

    # excepciones
    if not cliente_encontrado:
        raise HTTPException(
            status_code=400,
            detail=f"Error 400: No existe un cliente con ese id: {cliente_id}, debes crear el cliente.",
        )

    # CONSULTAR FACTURA
    # factura_encontrada = next((f for f in lista_facturas if f.id == factura_id), None)
    factura_encontrada = None
    for f in lista_facturas:
        if f.id == factura_id:
            factura_encontrada = f
            break

    # si la factura encontrada
    if factura_encontrada:
        # comprobar la factura con el id de cliente
        if factura_encontrada.cliente.id == cliente_id:
            # validar datos_transaccion
            transaccion_val = Transaccion.model_validate(datos_transaccion.model_dump())
            transaccion_val.id = len(lista_transacciones) + 1
            transaccion_val.factura_id = factura_id
            lista_transacciones.append(transaccion_val)

            factura_encontrada.transacciones.append(transaccion_val)
            mensaje = f"Transaccion agregada a factura {factura_encontrada.id}"
            factura_final = factura_encontrada
            return {"mensaje": mensaje, "factura": factura_final}
        else:
            mensaje = f"Se encontro la factura de id: {factura_id}, pero es de otro cliente id: {cliente_id}"
            factura_final = factura_encontrada
            return {"mensaje": mensaje, "factura encontrada": factura_final}
    else:
        # si no se ha encontrado una factura,

        # validamos datos de la transaccion, y despues creamos la factura
        transaccion_val = Transaccion.model_validate(datos_transaccion.model_dump())
        transaccion_val.id = len(lista_transacciones) + 1
        transaccion_val.factura_id = len(lista_facturas) + 1

        # creamos la factura(cliente, fecha, transacciones)
        factura = FacturaCrear(
            cliente=cliente_encontrado,
            fecha=str(datetime.now()),
            transacciones=[transaccion_val],
        )

        # datos_transaccion.vr_unitario * datos_transaccion.cantidad,
        factura_val = Factura.model_validate(factura.model_dump())
        factura_val.id = len(lista_facturas) + 1
        lista_facturas.append(factura_val)

        # Creamos la trasaccion (cantidad, vr_unitario, descripcion, factura_id)
        # transaccion_val = Transaccion.model_validate(datos_transaccion.model_dump())
        # transaccion_val.id = len(lista_transacciones) + 1
        # transaccion_val.factura_id = factura_id
        lista_transacciones.append(transaccion_val)

        return {
            "mensaje": f"Factura no existe con el id: {factura_id}, pero se creo la nueva factura",
            "facturas": transaccion_val,
        }
