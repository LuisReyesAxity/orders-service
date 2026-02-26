from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from orders_service.application.use_cases import OrderService
from orders_service.infrastructure.repository import InMemoryOrderRepository


# ---- SCHEMAS PYDANTIC - validan datos de entrada ----
class CreateOrderRequest(BaseModel):
    customer_id: str


class AddItemRequest(BaseModel):
    product_id: str
    product_name: str
    quantity: int
    unit_price: float


# ---- APP FASTAPI ----
app = FastAPI(title="Orders Service")

# Inyección de dependencias - como DI en C#
repository = InMemoryOrderRepository()
service = OrderService(repository)


# ---- ENDPOINTS ----
@app.post("/orders")
def create_order(request: CreateOrderRequest):
    order = service.create_order(request.customer_id)
    return {"id": order.id, "customer_id": order.customer_id, "status": order.status.value}


@app.get("/orders")
def get_all_orders():
    orders = service.get_all_orders()
    return [{"id": o.id, "customer_id": o.customer_id, "status": o.status.value, "total": o.total()} for o in orders]


@app.get("/orders/{order_id}")
def get_order(order_id: str):
    try:
        order = service.get_order(order_id)
        return {"id": order.id, "customer_id": order.customer_id, "status": order.status.value, "total": order.total()}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.post("/orders/{order_id}/items")
def add_item(order_id: str, request: AddItemRequest):
    try:
        order = service.add_item(order_id, request.product_id, request.product_name, request.quantity, request.unit_price)
        return {"id": order.id, "total": order.total()}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.post("/orders/{order_id}/confirm")
def confirm_order(order_id: str):
    try:
        order = service.confirm_order(order_id)
        return {"id": order.id, "status": order.status.value}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))