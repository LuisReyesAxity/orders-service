# Importamos las entidades del dominio para probarlas
from orders_service.domain.entities import Order, OrderItem, OrderStatus


def test_order_total():
    # Creamos una orden de prueba
    order = Order(id="1", customer_id="cliente-1")
    # Agregamos un item: 2 Widgets a $10 = $20
    order.add_item(OrderItem("p1", "Widget", quantity=2, unit_price=10.0))
    # Verificamos que el total sea correcto
    assert order.total() == 20.0


def test_order_confirm():
    order = Order(id="1", customer_id="cliente-1")
    order.confirm()  # Confirmamos la orden
    # Verificamos que el status cambió a CONFIRMED
    assert order.status == OrderStatus.CONFIRMED


def test_no_confirmar_dos_veces():
    order = Order(id="1", customer_id="cliente-1")
    order.confirm()  # Primera confirmación - ok
    try:
        order.confirm()  # Segunda confirmación - debe fallar
        assert False    # Si llega aquí, el test falla
    except ValueError:
        pass  # Si lanza ValueError, el test pasa - es lo esperado


def test_order_cancel():
    order = Order(id="1", customer_id="cliente-1")
    order.cancel()  # Cancelamos la orden
    # Verificamos que el status cambió a CANCELLED
    assert order.status == OrderStatus.CANCELLED