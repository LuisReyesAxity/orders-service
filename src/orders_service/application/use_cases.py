import uuid  # Para generar IDs únicos automáticamente, como Guid.NewGuid() en C#

from orders_service.domain.entities import Order, OrderItem  # Entidades del dominio
from orders_service.domain.ports.repository import OrderRepository  # El contrato/puerto


# Caso de uso - orquesta las operaciones del negocio
# Como un Service en C# - coordina el dominio con el repositorio
class OrderService:

    def __init__(self, repository: OrderRepository):
        # Recibe el repositorio por inyección de dependencias
        # No sabe si es SQLAlchemy o memoria - solo conoce el contrato
        self.repository = repository

    def create_order(self, customer_id: str) -> Order:
        # Crea una nueva orden con ID único
        order = Order(id=str(uuid.uuid4()), customer_id=customer_id)
        self.repository.save(order)  # La guarda usando el puerto
        return order

    def add_item(
        self,
        order_id: str,
        product_id: str,
        product_name: str,
        quantity: int,
        unit_price: float,
    ) -> Order:
        order = self.repository.get_by_id(order_id)  # Busca la orden
        if order is None:
            raise ValueError(f"Orden {order_id} no encontrada")  # Si no existe lanza error
        order.add_item(OrderItem(product_id, product_name, quantity, unit_price))  # Agrega el item
        self.repository.save(order)  # Guarda los cambios
        return order

    def confirm_order(self, order_id: str) -> Order:
        order = self.repository.get_by_id(order_id)  # Busca la orden
        if order is None:
            raise ValueError(f"Orden {order_id} no encontrada")
        order.confirm()  # Llama la regla de negocio del dominio
        self.repository.save(order)  # Guarda los cambios
        return order

    def get_order(self, order_id: str) -> Order:
        order = self.repository.get_by_id(order_id)  # Busca la orden
        if order is None:
            raise ValueError(f"Orden {order_id} no encontrada")
        return order

    def get_all_orders(self) -> list[Order]:
        return self.repository.get_all()  # Retorna todas las órdenes