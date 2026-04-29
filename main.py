from fastapi import FastAPI
from datetime import datetime
import zoneinfo
from pydantic import BaseModel

app = FastAPI()

class Cliente(BaseModel):
    id: int
    nombre: str
    descripcion: str | None
    email: str
    edad: int

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

@app.get("/hora/{iso_code}")
def hora(iso_code: str):
    iso = iso_code.upper()
    zona_lugar = ciudades.get(iso)
    tz = zoneinfo.ZoneInfo(zona_lugar)
    return{"Hora": datetime.now(tz)}

#reto, devolver la hora en formato de 24 horas
@app.post("/clientes")
def crear_cliente(datos_cliente:Cliente):
    return datos_cliente