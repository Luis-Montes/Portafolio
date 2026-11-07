from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean
from sqlalchemy.sql import func
from database.connection import Base

class Usuario(Base):
    __tablename__ = 'USUARIOS'

    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    rol = Column(String(30), default='OPERADOR')
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, server_default=func.now())

class Producto(Base):
    __tablename__ = 'PRODUCTOS'

    id_producto = Column(Integer, primary_key=True, autoincrement=True)
    sku = Column(String(50), unique=True, nullable=False)
    nombre = Column(String(150), nullable=False)
    tipo = Column(String(30), nullable=False)
    unidad_medida = Column(String(20), nullable=False)
    precio_compra = Column(Float, default=0.0)
    precio_venta = Column(Float, default=0.0)
    stock_minimo = Column(Float, default=0.0)
    stock_maximo = Column(Float, default=0.0)