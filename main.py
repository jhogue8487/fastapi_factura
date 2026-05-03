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
def hora(iso_code: str):
    iso = iso_code.upper()
    zona_lugar = ciudades.get(iso)
    tz = zoneinfo.ZoneInfo(zona_lugar)
    return{"Hora": datetime.now(tz)}

#codigo para id
cliente_id:int = 0


#es importante post(sin id), y get(con id)
@app.post("/clientes", response_model=Cliente)
def crear_cliente(datos_cliente: ClienteCrear):
    #aqui incrementamos id, y validar datos ingresados (simulando BD)
    cliente_val = Cliente.model_validate(datos_cliente.model_dump())
    cliente_val.id = cliente_id + 1
    return cliente_val#datos_cliente

@app.post("/transacciones")
def crear_transaccion(datos_transaccion: Transaccion):
    return datos_transaccion

@app.post("/facturas")
def crear_factura(datos_factura: Factura):
    return datos_factura