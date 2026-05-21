from fastapi import APIRouter
from ..modelos.clientes import Cliente, ClienteCrear, ClienteEditar
from ..listas import lista_clientes

ruta_clientes = APIRouter()


@ruta_clientes.post("/clientes", response_model=Cliente, tags=["Clientes"])
async def crear_cliente(datos_cliente: ClienteCrear):
    # aqui incrementamos id, y validar datos ingresados (simulando BD)
    cliente_val = Cliente.model_validate(datos_cliente.model_dump())
    # cliente_val.id = cliente_id + 1
    cliente_val.id = len(lista_clientes) + 1
    lista_clientes.append(cliente_val)
    return cliente_val  # datos_cliente


@ruta_clientes.get("/clientes", response_model=list[Cliente], tags=["Clientes"])
async def listar_clientes():
    # agregar un mensaje mas claro para el usuario, si no existen clientes.
    return lista_clientes


# RETO: obtener un cliente segun el id
@ruta_clientes.get("/clientes/{id}", tags=["Clientes"])
async def listar_cliente(id: int):
    # retornar mensajes claros al usuario, si no existe el cliente
    return [obj_c for obj_c in lista_clientes if obj_c.id == id]  # (pep8)


# RETO: editar
# @app.put("/clientes/{id}", response_model=Cliente)
@ruta_clientes.put("/clientes/{id}", tags=["Clientes"])
async def editar_clientes(id: int, datos_cliente: ClienteEditar):
    for i, obj_cliente in enumerate(lista_clientes):
        if obj_cliente.id == id:
            cliente_val = Cliente.model_validate(datos_cliente.model_dump())
            cliente_val.id = id
            lista_clientes[i] = cliente_val

    return {
        "mensaje": "Se actualizo el cliente satisfactoriamente.",
        "Cliente": cliente_val,
    }
    # return cliente_val


@ruta_clientes.delete("/clientes/{id}", tags=["Clientes"])
async def eliminar(id: int):
    for i, obj_cliente in enumerate(lista_clientes):
        if obj_cliente.id == id:
            obj_cliente_del = lista_clientes.pop(i)
            mensaje = "Cliente Eliminado."
        else:
            mensaje = "El ID del cliente no existe."
            obj_cliente_del = {}
    return {"mensaje": mensaje, "cliente": obj_cliente_del}
