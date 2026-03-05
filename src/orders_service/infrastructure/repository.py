from sqlalchemy import Column, String, create_engine  # Herramientas de SQLAlchemy, como EF en C#
from sqlalchemy.orm import DeclarativeBase, sessionmaker  # Base y sesión de SQLAlchemy

from orders_service.domain.entities import Order, OrderStatus  # Entidades del dominio


# Base para todos los modelos SQLAlchemy
# Como DbContext en C#
class Base(DeclarativeBase):
    pass


# Modelo de base de datos - representa la tabla "orders"
# Como una entidad con [Table] en C#
class OrderModel(Base):
    __tablename__ = "orders"               # Nombre de la tabla en la DB
    id = Column(String, primary_key=True)  # Columna ID, llave primaria
    customer_id = Column(String, nullable=False)  # Columna cliente, no puede ser vacío
    status = Column(String, default="pending")    # Columna estado, por defecto pending


# Conexión a la base de datos SQLite
engine = create_engine("sqlite:///orders.db")  # Crea la conexión, como connection string en C#
Base.metadata.create_all(engine)               # Crea las tablas si no existen
SessionLocal = sessionmaker(bind=engine)       # Fábrica de sesiones, como DbContext en C#


# ---- ADAPTADOR EN MEMORIA ----
# Implementa el puerto OrderRepository usando un diccionario
# Útil para pruebas, no necesita base de datos
class InMemoryOrderRepository:
    def __init__(self):
        self.orders: dict[str, Order] = {}  # Diccionario en memoria como almacén

    def save(self, order: Order) -> None:
        self.orders[order.id] = order  # Guarda la orden en el diccionario

    def get_by_id(self, order_id: str) -> Order | None:
        return self.orders.get(order_id)  # Busca por ID, retorna None si no existe

    def get_all(self) -> list[Order]:
        return list(self.orders.values())  # Retorna todas las órdenes


# ---- ADAPTADOR SQLALCHEMY ----
# Implementa el puerto OrderRepository usando SQLAlchemy
# Este es el adaptador real que guarda en base de datos
class SQLAlchemyOrderRepository:
    def __init__(self):
        self.session = SessionLocal()  # Abre la sesión de base de datos

    def save(self, order: Order) -> None:
        existing = self.session.query(OrderModel).filter_by(id=order.id).first()
        if existing:
            existing.status = order.status.value  # Si ya existe, actualiza el status
        else:
            self.session.add(
                OrderModel(                        # Si no existe, crea un nuevo registro
                    id=order.id,
                    customer_id=order.customer_id,
                    status=order.status.value,
                )
            )
        self.session.commit()  # Confirma los cambios en la DB, como SaveChanges() en C#

    def get_by_id(self, order_id: str) -> Order | None:
        model = self.session.query(OrderModel).filter_by(id=order_id).first()
        if not model:
            return None  # Si no encuentra retorna None
        order = Order(id=model.id, customer_id=model.customer_id)  # Convierte el modelo a entidad
        order.status = OrderStatus(model.status)  # Restaura el status del enum
        return order

    def get_all(self) -> list[Order]:
        models = self.session.query(OrderModel).all()  # Obtiene todos los registros
        orders = []
        for model in models:
            order = Order(id=model.id, customer_id=model.customer_id)  # Convierte cada modelo
            order.status = OrderStatus(model.status)
            orders.append(order)
        return orders