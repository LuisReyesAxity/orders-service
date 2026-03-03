from sqlalchemy import create_engine, Column, String, Float, Integer, Enum as SAEnum
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Crear conexión a la base de datos
engine = create_engine("sqlite:///orders.db")

# Crear sesión - como DbContext en C#
SessionLocal = sessionmaker(bind=engine)


# Base para todos los modelos - como DbContext en EF
class Base(DeclarativeBase):
    pass

# Modelo - como una entidad en EF
class OrderModel(Base):
    __tablename__ = "orders"
    
    id = Column(String, primary_key=True)
    customer_id = Column(String, nullable=False)
    status = Column(String, default="pending")



    # Crear tablas en la DB
Base.metadata.create_all(engine)

# Abrir sesión - como using(var context = new DbContext())
session = SessionLocal()

# Crear una orden
nueva_orden = OrderModel(id="2", customer_id="cliente-1", status="pending")

# Guardar en DB
session.add(nueva_orden)
session.commit()

# Consultar
orden = session.query(OrderModel).filter_by(id="1").first()
print(f"Orden encontrada: {orden.customer_id} - {orden.status}")

# Actualizar
orden.status = "confirmed"
session.commit()
print(f"Status actualizado: {orden.status}")

# Eliminar
session.delete(orden)
session.commit()
print("Orden eliminada")

# Verificar que ya no existe
orden_eliminada = session.query(OrderModel).filter_by(id="1").first()
print(f"Orden después de eliminar: {orden_eliminada}")