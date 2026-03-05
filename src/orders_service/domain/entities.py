from dataclasses import dataclass, field  # Para crear clases sin escribir el constructor manualmente
from datetime import datetime             # Para manejar fechas, como DateTime en C#
from enum import Enum                     # Para crear enumeraciones, como enum en C#


# Los posibles estados de una orden
class OrderStatus(Enum):
    PENDING = "pending"       # Orden creada, esperando confirmación
    CONFIRMED = "confirmed"   # Orden confirmada
    CANCELLED = "cancelled"   # Orden cancelada


# Un producto dentro de la orden
# @dataclass genera el constructor automáticamente - como record en C#
@dataclass
class OrderItem:
    product_id: str      # ID del producto
    product_name: str    # Nombre del producto
    quantity: int        # Cantidad
    unit_price: float    # Precio unitario

    def subtotal(self) -> float:
        return self.quantity * self.unit_price  # Calcula el subtotal de este item


# La orden principal
@dataclass
class Order:
    id: str                    # ID único de la orden
    customer_id: str           # ID del cliente
    status: OrderStatus = OrderStatus.PENDING                    # Estado inicial siempre es PENDING
    created_at: datetime = field(default_factory=datetime.utcnow) # Fecha de creación automática
    items: list[OrderItem] = field(default_factory=list)          # Lista de items, inicia vacía

    def add_item(self, item: OrderItem) -> None:
        self.items.append(item)  # Agrega un item a la orden

    def total(self) -> float:
        return sum(item.subtotal() for item in self.items)  # Suma todos los subtotales

    def confirm(self) -> None:
        if self.status != OrderStatus.PENDING:
            raise ValueError("Solo se puede confirmar una orden pendiente")  # Regla de negocio
        self.status = OrderStatus.CONFIRMED  # Cambia el estado a confirmado

    def cancel(self) -> None:
        if self.status == OrderStatus.CANCELLED:
            raise ValueError("La orden ya está cancelada")  # Regla de negocio
        self.status = OrderStatus.CANCELLED  # Cambia el estado a cancelado