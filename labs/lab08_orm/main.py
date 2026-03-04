from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Conexión a la base de datos
engine = create_engine("sqlite:///orders.db")
SessionLocal = sessionmaker(bind=engine)


# Base para todos los modelos
class Base(DeclarativeBase):
    pass


# Modelo
class OrderModel(Base):
    __tablename__ = "orders"

    id = Column(String, primary_key=True)
    customer_id = Column(String, nullable=False)
    status = Column(String, default="pending")


# Crear tablas
Base.metadata.create_all(engine)


# Solo ejecuta el CRUD si corres este archivo directamente
if __name__ == "__main__":
    session = SessionLocal()

    nueva_orden = OrderModel(id="3", customer_id="cliente-1", status="pending")
    session.add(nueva_orden)
    session.commit()

    orden = session.query(OrderModel).filter_by(id="3").first()
    print(f"Orden encontrada: {orden.customer_id} - {orden.status}")

    orden.status = "confirmed"
    session.commit()
    print(f"Status actualizado: {orden.status}")

    session.delete(orden)
    session.commit()
    print("Orden eliminada")

    orden_eliminada = session.query(OrderModel).filter_by(id="3").first()
    print(f"Orden después de eliminar: {orden_eliminada}")