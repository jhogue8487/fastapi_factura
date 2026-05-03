from fastapi import FastAPI
from datetime import datetime
import zoneinfo
from modelos.cliente import Cliente, ClienteCrear
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
cliente_id:int = 0
#crear una lista para guardar datos
lista_clientes:list[Cliente] = []

#es importante post(sin id), y get(con id)
@app.post("/clientes", response_model=Cliente)
async def crear_cliente(datos_cliente: ClienteCrear):
    #aqui incrementamos id, y validar datos ingresados (simulando BD)
    cliente_val = Cliente.model_validate(datos_cliente.model_dump())
    #cliente_val.id = cliente_id + 1
    cliente_val.id = len(lista_clientes)+1
    lista_clientes.append(cliente_val)
    return cliente_val#datos_cliente

@app.get("/clientes")
async def listar_clientes():
    return lista_clientes

@app.post("/transacciones")
async def crear_transaccion(datos_transaccion: Transaccion):
    return datos_transaccion

@app.post("/facturas")
async def crear_factura(datos_factura: Factura):
    return datos_factura