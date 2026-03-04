from orders_service.domain.entities import Order, OrderItem, OrderStatus


def test_order_total():
    order = Order(id="1", customer_id="cliente-1")
    order.add_item(OrderItem("p1", "Widget", quantity=2, unit_price=10.0))
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
        assert False
    except ValueError:
        pass


def test_order_cancel():
    order = Order(id="1", customer_id="cliente-1")
    order.cancel()
    assert order.status == OrderStatus.CANCELLED