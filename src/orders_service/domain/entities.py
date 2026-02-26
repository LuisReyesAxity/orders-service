from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


# Estado de la orden
class OrderStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"


# Item de la orden
@dataclass
class OrderItem:
    product_id: str
    product_name: str
    quantity: int
    unit_price: float

    def subtotal(self) -> float:
        return self.quantity * self.unit_price


# Orden principal
@dataclass
class Order:
    id: str
    customer_id: str
    status: OrderStatus = OrderStatus.PENDING
    created_at: datetime = field(default_factory=datetime.utcnow)
    items: list[OrderItem] = field(default_factory=list)

    def add_item(self, item: OrderItem) -> None:
        self.items.append(item)

    def total(self) -> float:
        return sum(item.subtotal() for item in self.items)

    def confirm(self) -> None:
        if self.status != OrderStatus.PENDING:
            raise ValueError("Solo se puede confirmar una orden pendiente")
        self.status = OrderStatus.CONFIRMED

    def cancel(self) -> None:
        if self.status == OrderStatus.CANCELLED:
            raise ValueError("La orden ya está cancelada")
        self.status = OrderStatus.CANCELLED