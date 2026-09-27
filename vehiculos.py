from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import Session

from database import Base, get_db

router = APIRouter()



class Vehiculo(Base):
    __tablename__ = "vehiculos"

    id = Column(Integer, primary_key=True, index=True)
    placa = Column(String, nullable=False)
    marca = Column(String, nullable=False)
    modelo_anio = Column(Integer, nullable=False)
    precio_alquiler = Column(Float, nullable=False)


@router.get("/inventario-rodante/filtrado-especial")
def ejecutar_busqueda_compleja_autos(
    tope_precio: Optional[float] = None,
    corte_modelo: Optional[int] = None,
    db: Session = Depends(get_db),
):
    consulta = db.query(Vehiculo)

    if tope_precio is not None:
        consulta = consulta.filter(Vehiculo.precio_alquiler <= tope_precio)

    if corte_modelo is not None:
        consulta = consulta.filter(Vehiculo.modelo_anio >= corte_modelo)

    resultado_matriz_vehiculos = consulta.all()

    if not resultado_matriz_vehiculos:
        raise HTTPException(
            status_code=404,
            detail="No hay vehículos que cumplan con los criterios especificos",
        )

    return resultado_matriz_vehiculos
