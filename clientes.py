from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session

from database import Base, get_db

router = APIRouter()



class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    saldo_pendiente = Column(Float, nullable=False, default=0)
    activo = Column(Boolean, default=True)



@router.delete("/clientes/baja-logica/{identificador_cliente}")
def procesar_inactivacion_cuenta_usuario(
    identificador_cliente: int, db: Session = Depends(get_db)
):
    registro_usuario_afiliado = db.query(Cliente).filter(
        Cliente.id == identificador_cliente
    ).first()

    if registro_usuario_afiliado is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    if registro_usuario_afiliado.saldo_pendiente > 0:
        raise HTTPException(
            status_code=400,
            detail="No se puede desactivar un cliente con saldo pendiente",
        )

    registro_usuario_afiliado.activo = False
    db.commit()

    return {
        "estado_operacion": "proceso_exitoso",
        "cuenta_afectada": identificador_cliente,
    }
