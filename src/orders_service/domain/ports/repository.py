from typing import Protocol  # Para crear interfaces, como Interface en C#
from orders_service.domain.entities import Order  # Importamos la entidad Order


# Puerto - es el contrato que debe cumplir cualquier repositorio
# Como una Interface en C# - define QUÉ se puede hacer, no CÓMO
# El dominio solo conoce este contrato, no sabe si es SQLAlchemy o memoria
class OrderRepository(Protocol):

    def save(self, order: Order) -> None: ...       # Guardar una orden

    def get_by_id(self, order_id: str) -> Order | None: ...  # Buscar por ID, puede retornar None

    def get_all(self) -> list[Order]: ...           # Obtener todas las órdenes