from dataclasses import dataclass, field
from enum import Enum
from pydantic import BaseModel


# ---- ENUM - como enum en C# ----
class OrderStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"


# ---- DATACLASS - como record en C# ----
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


# ---- PROBAMOS ----
print("--- Orden ---")
order = Order(id="1", customer_id="cliente-1")
order.add_item(OrderItem("Widget", quantity=2, unit_price=10.0))
order.add_item(OrderItem("Gadget", quantity=1, unit_price=25.0))
print(f"Total: ${order.total()}")
order.confirm()
print(f"Status: {order.status}")


# ---- PYDANTIC - validación de datos ----
# Como Data Annotations en C#
class OrderItemIn(BaseModel):
    product_name: str
    quantity: int
    unit_price: float


class OrderIn(BaseModel):
    customer_id: str
    items: list[OrderItemIn]


# Datos válidos
print("\n--- Pydantic ---")
orden = OrderIn(
    customer_id="cliente-1",
    items=[
        OrderItemIn(product_name="Widget", quantity=2, unit_price=10.0)
    ]
)
print(f"Orden recibida: {orden}")

# Datos inválidos - pydantic lanza error automático
print("\n--- Pydantic error ---")
try:
    orden_mala = OrderItemIn(
        product_name="Widget",
        quantity="no soy un número",  # error a propósito
        unit_price=10.0
    )
except Exception as e:
    print(f"Error capturado: {e}")









    # ---- HERENCIA - como herencia en C# ----
# DiscountOrder hereda todo de Order y agrega descuento
@dataclass
class DiscountOrder(Order):
    discount: float = 0.0

    def total(self) -> float:
        # super() llama al total() del padre
        return super().total() * (1 - self.discount)


print("\n--- Herencia ---")
order2 = DiscountOrder(id="2", customer_id="cliente-2", discount=0.10)
order2.add_item(OrderItem("Widget", quantity=2, unit_price=10.0))
print(f"Total con 10% descuento: ${order2.total()}")


# ---- DUNDER METHODS ----
# Son métodos especiales que Python llama automáticamente
# __str__ = override de ToString() en C#
# __eq__ = override de Equals() en C#
@dataclass
class Product:
    name: str
    price: float

    def __str__(self) -> str:
        return f"Producto: {self.name} - ${self.price}"

    def __eq__(self, other) -> bool:
        return self.name == other.name


print("\n--- Dunder methods ---")
p1 = Product("Widget", 10.0)
p2 = Product("Gadget", 25.0)
print(p1)                           # llama __str__ automáticamente
print(f"Son iguales: {p1 == p2}")   # llama __eq__ automáticamente

# ---- ATTRS ----
# Similar a dataclass pero con más opciones de validación
import attr

@attr.s
class Customer:
    name: str = attr.ib()
    email: str = attr.ib()
    age: int = attr.ib()

    @age.validator
    def validar_edad(self, attribute, value):
        if value < 18:
            raise ValueError("El cliente debe ser mayor de edad")


print("\n--- Attrs ---")
cliente = Customer(name="Luis", email="luis@mail.com", age=25)
print(f"Cliente: {cliente}")

# Edad inválida
try:
    cliente_malo = Customer(name="Juan", email="juan@mail.com", age=15)
except ValueError as e:
    print(f"Error: {e}")