from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session

from database import Base, get_db

router = APIRouter()

class Sensor(Base):
    __tablename__ = "sensores"

    id = Column(Integer, primary_key=True, index=True)
    ubicacion = Column(String, nullable=False)
    temperatura_actual = Column(Float, nullable=False)
    estado_alerta = Column(Boolean, default=False)


class SensorActualizacion(BaseModel):
    temperatura_actual: float


def evaluar_salto_termico(temp_vieja: float, temp_nueva: float) -> bool:
    return abs(temp_nueva - temp_vieja) > 30


@router.patch("/sensores/nodo/{id_nodo_sensor}")
def actualizar_lectura_termica_nodo(
    id_nodo_sensor: int,
    datos: SensorActualizacion,
    db: Session = Depends(get_db),
):
    instancia_sensor_objeto = db.query(Sensor).filter(
        Sensor.id == id_nodo_sensor
    ).first()

    if instancia_sensor_objeto is None:
        raise HTTPException(status_code=404, detail="Sensor no encontrado")

    hay_salto = evaluar_salto_termico(
        instancia_sensor_objeto.temperatura_actual, datos.temperatura_actual
    )

    instancia_sensor_objeto.estado_alerta = True if hay_salto else False
    instancia_sensor_objeto.temperatura_actual = datos.temperatura_actual

    db.commit()
    db.refresh(instancia_sensor_objeto)

    return instancia_sensor_objeto
