from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from orders_service.domain.entities import Order, OrderStatus


# Base para modelos SQLAlchemy
class Base(DeclarativeBase):
    pass


# Modelo de base de datos
class OrderModel(Base):
    __tablename__ = "orders"
    id = Column(String, primary_key=True)
    customer_id = Column(String, nullable=False)
    status = Column(String, default="pending")


# Configuración de la base de datos
engine = create_engine("sqlite:///orders.db")
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)


# ---- ADAPTADOR EN MEMORIA ----
class InMemoryOrderRepository:
    def __init__(self):
        self.orders: dict[str, Order] = {}

    def save(self, order: Order) -> None:
        self.orders[order.id] = order

    def get_by_id(self, order_id: str) -> Order | None:
        return self.orders.get(order_id)

    def get_all(self) -> list[Order]:
        return list(self.orders.values())


# ---- ADAPTADOR SQLALCHEMY ----
class SQLAlchemyOrderRepository:
    def __init__(self):
        self.session = SessionLocal()

    def save(self, order: Order) -> None:
        existing = self.session.query(OrderModel).filter_by(id=order.id).first()
        if existing:
            existing.status = order.status.value
        else:
            self.session.add(OrderModel(
                id=order.id,
                customer_id=order.customer_id,
                status=order.status.value
            ))
        self.session.commit()

    def get_by_id(self, order_id: str) -> Order | None:
        model = self.session.query(OrderModel).filter_by(id=order_id).first()
        if not model:
            return None
        order = Order(id=model.id, customer_id=model.customer_id)
        order.status = OrderStatus(model.status)
        return order

    def get_all(self) -> list[Order]:
        models = self.session.query(OrderModel).all()
        orders = []
        for model in models:
            order = Order(id=model.id, customer_id=model.customer_id)
            order.status = OrderStatus(model.status)
            orders.append(order)
        return orders