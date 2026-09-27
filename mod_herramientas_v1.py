from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import Session

from database import Base, get_db

router = APIRouter()



class Herramienta(Base):
    __tablename__ = "herramientas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    precio_compra = Column(Float, nullable=False)
    anios_vida_util = Column(Integer, nullable=False)
    depreciacion_anual = Column(Float, nullable=False)



class HerramientaEntrada(BaseModel):
    nombre: str
    costo_adquisicion_cop: float
    anios_vida_util: int


@router.post("/herramientas")
def registrar_elemento_taller_adso(
    datos: HerramientaEntrada, db: Session = Depends(get_db)
):
    conexion_activa_orm = db

    if datos.anios_vida_util <= 0:
        raise HTTPException(
            status_code=400,
            detail="anios_vida_util debe ser mayor a 0",
        )

    depreciacion_anual = datos.costo_adquisicion_cop / datos.anios_vida_util

    nueva_herramienta = Herramienta(
        nombre=datos.nombre,
        precio_compra=datos.costo_adquisicion_cop,
        anios_vida_util=datos.anios_vida_util,
        depreciacion_anual=depreciacion_anual,
    )

    conexion_activa_orm.add(nueva_herramienta)
    conexion_activa_orm.commit()
    conexion_activa_orm.refresh(nueva_herramienta)

    return nueva_herramienta
