from fastapi import APIRouter
from datetime import datetime
from zoneinfo import zoneinfo

router = APIRouter()


@router.get("/")
def inicio():
    return {"mensaje": "hola mundo"}


ciudades = {
    "AR": "America/Argentina/Buenos_Aires",
    "GT": "América/Guatemala",
    "MX": "America/Mexico_City",
    "CO": "America/Bogota",
    "ES": "España",
    "CL": "Chile",
}


# reto, devolver la hora en formato de 24 horas
# esta editado para regresra horas
@router.get("/hora/{iso_code}")
async def hora(iso_code: str):
    iso = iso_code.upper()
    zona_lugar = ciudades.get(iso)
    tz = zoneinfo.ZoneInfo(zona_lugar)
    return {"Hora": datetime.now(tz)}
