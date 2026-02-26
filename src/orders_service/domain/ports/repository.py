from typing import Protocol
from orders_service.domain.entities import Order


# ---- PUERTO - contrato que debe cumplir cualquier repositorio ----
# Como una Interface en C#
class OrderRepository(Protocol):

    def save(self, order: Order) -> None:
        ...

    def get_by_id(self, order_id: str) -> Order | None:
        ...

    def get_all(self) -> list[Order]:
        ...