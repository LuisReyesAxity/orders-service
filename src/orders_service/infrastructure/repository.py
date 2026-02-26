from orders_service.domain.entities import Order
from orders_service.domain.ports.repository import OrderRepository


# ---- ADAPTADOR EN MEMORIA ----
# Como un repositorio en memoria en C#
# Implementa el puerto OrderRepository
class InMemoryOrderRepository:

    def __init__(self):
        self.orders: dict[str, Order] = {}

    def save(self, order: Order) -> None:
        self.orders[order.id] = order

    def get_by_id(self, order_id: str) -> Order | None:
        return self.orders.get(order_id)

    def get_all(self) -> list[Order]:
        return list(self.orders.values())