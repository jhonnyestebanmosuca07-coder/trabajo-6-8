from fastapi import FastAPI

from database import Base, engine
import mod_herramientas_v1
import vehiculos
import sensores
import clientes
import productos

Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Taller - Ejercicios ADSO")

app.include_router(mod_herramientas_v1.router, tags=["Herramientas"])
app.include_router(vehiculos.router, tags=["Vehiculos"])
app.include_router(sensores.router, tags=["Sensores"])
app.include_router(clientes.router, tags=["Clientes"])
app.include_router(productos.router, tags=["Productos"])
