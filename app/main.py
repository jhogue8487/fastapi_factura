from fastapi import FastAPI, HTTPException, status
from .routers import clientes, facturas, transacciones
from .conexion_bd import crear_tablas

app = FastAPI(lifespan=crear_tablas)


app.include_router(clientes.ruta_clientes)
app.include_router(facturas.ruta_facturas)
app.include_router(transacciones.ruta_transanccciones)
