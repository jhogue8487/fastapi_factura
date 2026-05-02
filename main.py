from fastapi import FastAPI
from datetime import datetime
import zoneinfo
from modelos.cliente import Cliente
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


@app.post("/clientes")
def crear_cliente(datos_cliente: Cliente):
    return datos_cliente

@app.post("/transacciones")
def crear_transaccion(datos_transaccion: Transaccion):
    return datos_transaccion

@app.post("/facturas")
def crear_factura(datos_factura: Factura):
    return datos_factura