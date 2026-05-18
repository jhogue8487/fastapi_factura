from fastapi import FastAPI, HTTPException, status
from datetime import datetime
import zoneinfo
from modelos.cliente import Cliente, ClienteCrear, ClienteEditar
from modelos.transaccion import Transaccion, TransaccionCrear
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

@app.get("/clientes", response_model=list[Cliente], tags=["Clientes"])
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
    return [obj_c for obj_c in lista_clientes if obj_c.id ==id]#(pep8)

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


#Relacionar los modelos de facturas y transacciones
#capturar excepciones de fastapi con httpexcepcion, o try except

lista_facturas:list[Factura]=[]

@app.post("/transacciones/{factura_id}", response_model=Factura)
def crear_transaccion(factura_id:int, datos_transaccion: TransaccionCrear, cliente_id:int):
    #Consular si cliente_id existe; para consultar si tiene facturas con ese id y adicionar una transaccion o crear nueva factura.
    #cliente_encontrado = next((c for c in db_clientes if c.id == cliente_id), None)
    cliente_encontrado = None
    for c in lista_clientes:
        if c.id == cliente_id:
            cliente_encontrado = c
            break
    
    #excepciones
    if not cliente_encontrado:
        raise HTTPException(status_code=400, detail="Error 400: No existe un cliente con ese id.")
    
    #consultar facturas
    #factura_existente = next((f for f in lista_facturas if f.id == factura_id), None)
    factura_encontrada = None
    for f in lista_facturas:
        if f.id == factura_id:
            factura_encontrada = f
            break
    
    #factura_final, mensaje = "", ""
    if factura_encontrada:
        #comprobar la factura con el id de cliente
        if factura_encontrada and factura_encontrada.id == cliente_id:
            factura_encontrada.transacciones.extend(datos_transaccion)
            factura_encontrada.cantidad_total()
            mensaje = f"Transaccion agregada a factura {factura_encontrada.id}"
            factura_final = factura_encontrada
            return {"mensaje": mensaje, "factura": factura_final}
        else:
            #creamos una nueva factura
            # factura_nueva = Factura()
            # factura_nueva = 
            mensaje ="en proceso de dsarrollo por else"
            factura_final = "En desarrollo"
            return {"mensaje": mensaje, "factura": factura_final}
    