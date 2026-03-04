from dataclasses import dataclass, field
from enum import Enum


class OrderStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"


@dataclass
class OrderItem:
    product_name: str
    quantity: int
    unit_price: float

    def subtotal(self) -> float:
        return self.quantity * self.unit_price


@dataclass
class Order:
    id: str
    customer_id: str
    status: OrderStatus = OrderStatus.PENDING
    items: list[OrderItem] = field(default_factory=list)

    def add_item(self, item: OrderItem) -> None:
        self.items.append(item)

    def total(self) -> float:
        return sum(item.subtotal() for item in self.items)

    def confirm(self) -> None:
        if self.status != OrderStatus.PENDING:
            raise ValueError("Solo se puede confirmar una orden pendiente")
        self.status = OrderStatus.CONFIRMED


# ---- TESTS ----
def test_order_total():
    order = Order(id="1", customer_id="cliente-1")
    order.add_item(OrderItem("Widget", quantity=2, unit_price=10.0))
    assert order.total() == 20.0


def test_order_confirm():
    order = Order(id="1", customer_id="cliente-1")
    order.confirm()
    assert order.status == OrderStatus.CONFIRMED


def test_no_confirmar_dos_veces():
    order = Order(id="1", customer_id="cliente-1")
    order.confirm()
    try:
        order.confirm()
        assert False, "Debería haber lanzado error"
    except ValueError:
        pass
