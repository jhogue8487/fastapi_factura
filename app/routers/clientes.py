from fastapi import APIRouter, HTTPException, status
from ..modelos.clientes import Cliente, ClienteCrear, ClienteEditar
from ..listas import lista_clientes
from ..conexion_bd import Sesion_dependencia
from sqlmodel import select

ruta_clientes = APIRouter()


@ruta_clientes.post("/clientes", response_model=Cliente, tags=["Clientes"])
async def crear_cliente(datos_cliente: ClienteCrear, sesion: Sesion_dependencia):
    # aqui incrementamos id, y validar datos ingresados (simulando BD)
    cliente_val = Cliente.model_validate(datos_cliente.model_dump())
    sesion.add(cliente_val)
    sesion.commit()
    sesion.refresh(cliente_val)
    # cliente_val.id = cliente_id + 1
    # cliente_val.id = len(lista_clientes) + 1
    # lista_clientes.append(cliente_val)
    return cliente_val  # datos_cliente


@ruta_clientes.get("/clientes", response_model=list[Cliente], tags=["Clientes"])
async def listar_clientes(sesion: Sesion_dependencia):
    # agregar un mensaje mas claro para el usuario, si no existen clientes.
    # podemos crera una variable o retornar directamente
    return sesion.exec(select(Cliente)).all()
    # return lista_clientes


# RETO: obtener un cliente segun el id
@ruta_clientes.get("/clientes/{id}", tags=["Clientes"])
async def listar_cliente(id: int, sesion: Sesion_dependencia):
    # retornar mensajes claros al usuario, si no existe el cliente
    # return [obj_c for obj_c in lista_clientes if obj_c.id == id]  # (pep8)
    # con bd
    cliente_bd = sesion.get(Cliente, id)
    if not cliente_bd:
        raise HTTPException(
            status_code=404, detail=f"El cliente con id {id} no existe."
        )
    return cliente_bd


# RETO: editar
# @app.put("/clientes/{id}", response_model=Cliente)
@ruta_clientes.patch("/clientes/{id}", tags=["Clientes"])
async def editar_clientes(
    id: int, datos_cliente: ClienteEditar, sesion: Sesion_dependencia
):
    # for i, obj_cliente in enumerate(lista_clientes):
    #     if obj_cliente.id == id:
    #         cliente_val = Cliente.model_validate(datos_cliente.model_dump())
    #         cliente_val.id = id
    #         lista_clientes[i] = cliente_val

    # return {
    #     "mensaje": "Se actualizo el cliente satisfactoriamente.",
    #     "Cliente": cliente_val,
    # }
    # con bd
    cliente_bd = sesion.get(Cliente, id)
    if not cliente_bd:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cliente con id {id} no existe.",
        )
    datos_cliente_dict = datos_cliente.model_dump(exclude_unset=True)
    cliente_bd.sqlmodel_update(datos_cliente_dict)
    sesion.add(cliente_bd)
    sesion.commit()
    sesion.refresh(cliente_bd)
    return cliente_bd


@ruta_clientes.delete("/clientes/{id}", tags=["Clientes"])
async def eliminar(id: int, sesion: Sesion_dependencia):
    # for i, obj_cliente in enumerate(lista_clientes):
    #     if obj_cliente.id == id:
    #         obj_cliente_del = lista_clientes.pop(i)
    #         mensaje = "Cliente Eliminado."
    #     else:
    #         mensaje = "El ID del cliente no existe."
    #         obj_cliente_del = {}
    # return {"mensaje": mensaje, "cliente": obj_cliente_del}
    cliente_bd = sesion.get(Cliente, id)
    if not cliente_bd:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El cliente con id {id} no existe.",
        )
    sesion.delete(cliente_bd)
    sesion.commit()
    return {"mensaje": "Cliente eliminado correctamente."}
