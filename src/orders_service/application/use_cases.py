import uuid
from orders_service.domain.entities import Order, OrderItem
from orders_service.domain.ports.repository import OrderRepository


# ---- CASOS DE USO - la lógica de la aplicación ----
# Como un Service en C#
class OrderService:

    def __init__(self, repository: OrderRepository):
        self.repository = repository

    def create_order(self, customer_id: str) -> Order:
        order = Order(
            id=str(uuid.uuid4()),
            customer_id=customer_id
        )
        self.repository.save(order)
        return order

    def add_item(self, order_id: str, product_id: str, product_name: str, quantity: int, unit_price: float) -> Order:
        order = self.repository.get_by_id(order_id)
        if order is None:
            raise ValueError(f"Orden {order_id} no encontrada")
        order.add_item(OrderItem(product_id, product_name, quantity, unit_price))
        self.repository.save(order)
        return order

    def confirm_order(self, order_id: str) -> Order:
        order = self.repository.get_by_id(order_id)
        if order is None:
            raise ValueError(f"Orden {order_id} no encontrada")
        order.confirm()
        self.repository.save(order)
        return order

    def get_order(self, order_id: str) -> Order:
        order = self.repository.get_by_id(order_id)
        if order is None:
            raise ValueError(f"Orden {order_id} no encontrada")
        return order

    def get_all_orders(self) -> list[Order]:
        return self.repository.get_all()