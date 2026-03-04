from dataclasses import dataclass, field
from enum import Enum

# ---- ENUM (Igual que en C#) ----
# Define estados fijos para evitar errores de escritura (strings mágicos).
class OrderStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"


# ---- DATACLASS (Como un 'record' o una clase DTO en C#) ----
# @dataclass te ahorra escribir el constructor __init__ a mano.
@dataclass
class OrderItem:
    product_name: str
    quantity: int
    unit_price: float

    # Un método simple que calcula datos basados en los atributos.
    def subtotal(self) -> float:
        return self.quantity * self.unit_price


@dataclass
class Order:
    id: str
    customer_id: str
    # Valor por defecto: empieza como PENDING.
    status: OrderStatus = OrderStatus.PENDING
    # field(default_factory=list) es como inicializar una List<OrderItem>() en el constructor.
    items: list[OrderItem] = field(default_factory=list)

    # LÓGICA DE NEGOCIO: Métodos que cambian el estado del objeto.
    def add_item(self, item: OrderItem) -> None:
        self.items.append(item)

    def total(self) -> float:
        # Suma todos los subtotales. Es como un .Sum(x => x.Subtotal) en LINQ.
        return sum(item.subtotal() for item in self.items)

    def confirm(self) -> None:
        # Regla de negocio: No puedes confirmar algo que ya está confirmado o cancelado.
        if self.status != OrderStatus.PENDING:
            raise ValueError("Solo se puede confirmar una orden pendiente")
        self.status = OrderStatus.CONFIRMED


# ---- TESTS (Como pruebas unitarias con xUnit/NUnit) ----
# Estas funciones verifica la lógica sea correcta.

def test_order_total():
    order = Order(id="1", customer_id="cliente-1")
    order.add_item(OrderItem("Widget", quantity=2, unit_price=10.0))
    # 'assert' verifica que la condición sea verdadera. Si falla, el test falla.
    assert order.total() == 20.0


def test_order_confirm():
    order = Order(id="1", customer_id="cliente-1")
    order.confirm()
    assert order.status == OrderStatus.CONFIRMED


def test_no_confirmar_dos_veces():
    order = Order(id="1", customer_id="cliente-1")
    order.confirm()
    try:
        order.confirm() # Esto debería fallar según nuestra regla en la clase.
        assert False, "Debería haber lanzado error"
    except ValueError:
        # Si entra aquí, el test pasó porque esperábamos el error.
        pass