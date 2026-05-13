from fastapi import FastAPI, HTTPException
from datetime import datetime
import zoneinfo
from modelos.cliente import Cliente, ClienteCrear, ClienteEditar
from modelos.transaccion import Transaccion
from modelos.factura import Factura

app = FastAPI()

@app.get("/")
def inicio():
    return {"mensaje": "hola mundo"}

ciudades = {
    "AR": "America/Argentina/Buenos_Aires",
    "GT": "América/Guatemala",
    "MX": "America/Mexico_City",
    "CO": "America/Bogota",
    "ES": "España",
    "CL": "Chile"
}

#reto, devolver la hora en formato de 24 horas
#esta editado para regresra horas
@app.get("/hora/{iso_code}")
async def hora(iso_code: str):
    iso = iso_code.upper()
    zona_lugar = ciudades.get(iso)
    tz = zoneinfo.ZoneInfo(zona_lugar)
    return{"Hora": datetime.now(tz)}

#codigo para id, despues se eliminara esta variable por la lista de clientes
#cliente_id:int = 0
#crear una lista para guardar datos
lista_clientes:list[Cliente] = []

#es importante post(sin id), y get(con id)
@app.post("/clientes", response_model=Cliente, tags=["Clientes"])
async def crear_cliente(datos_cliente: ClienteCrear):
    #aqui incrementamos id, y validar datos ingresados (simulando BD)
    cliente_val = Cliente.model_validate(datos_cliente.model_dump())
    #cliente_val.id = cliente_id + 1
    cliente_val.id = len(lista_clientes)+1
    lista_clientes.append(cliente_val)
    return cliente_val#datos_cliente

@app.get("/clientes", tags=["Clientes"])
async def listar_clientes():
    #agregar un mensaje mas claro para el usuario, si no existen clientes.
    return lista_clientes

@app.post("/transacciones")
async def crear_transaccion(datos_transaccion: Transaccion):
    return datos_transaccion

@app.post("/facturas")
async def crear_factura(datos_factura: Factura):
    return datos_factura

#RETO: obtener un cliente segun el id
@app.get("/clientes/{id}")
async def listar_cliente(id:int):
    #retornar mensajes claros al usuario, si no existe el cliente
    return [d for d in lista_clientes if d.id ==id]

#RETO: editar
#@app.put("/clientes/{id}", response_model=Cliente)
@app.put("/clientes/{id}")
async def editar_clientes(id:int, datos_cliente:ClienteEditar):
    for i, obj_cliente in enumerate(lista_clientes):
        if obj_cliente.id == id:
            cliente_val = Cliente.model_validate(datos_cliente.model_dump())
            cliente_val.id = id
            lista_clientes[i] = cliente_val
    
    return {"mensaje":"Se actualizo el cliente satisfactoriamente.","Cliente": cliente_val}
    #return cliente_val

@app.delete("/clientes/{id}")
def eliminar(id:int):
    for i, obj_cliente in enumerate(lista_clientes):
        if obj_cliente.id == id:
            obj_cliente_del = lista_clientes.pop(i)
            mensaje="Cliente Eliminado."
        else:
            mensaje ="El ID del cliente no existe."
            obj_cliente_del={}
    return {"mensaje":mensaje, "cliente": obj_cliente_del}
