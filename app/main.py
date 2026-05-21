from fastapi import FastAPI, HTTPException, status
from .routers import clientes, facturas, transacciones

app = FastAPI()
app.include_router(clientes.ruta_clientes)
app.include_router(facturas.ruta_facturas)
app.include_router(transacciones.ruta_transanccciones)
