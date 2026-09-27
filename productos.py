from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import Session

from database import Base, get_db

router = APIRouter()


class Producto(Base):
    __tablename__ = "tb_catalogo_productos_adso"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, nullable=False)
    precio_base = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    precio_final = Column(Float, nullable=False)


class EstructuraEntradaCatalogo(BaseModel):
    codigo: str
    precio_base: float
    stock: int



@router.put("/productos/{id}")
def reemplazar_registro_mercancia_total(
    id: int, datos: EstructuraEntradaCatalogo, db: Session = Depends(get_db)
):
    producto_existente = db.query(Producto).filter(Producto.id == id).first()

    if producto_existente is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    try:
        if datos.stock > 100:
            precio_final = datos.precio_base * 0.85
        else:
            precio_final = datos.precio_base
    except (TypeError, ZeroDivisionError, ArithmeticError) as error:
        raise HTTPException(
            status_code=400,
            detail=f"Error al calcular el precio final: {error}",
        )

    producto_existente.codigo = datos.codigo
    producto_existente.precio_base = datos.precio_base
    producto_existente.stock = datos.stock
    producto_existente.precio_final = precio_final

    db.commit()
    db.refresh(producto_existente)

    return producto_existente
