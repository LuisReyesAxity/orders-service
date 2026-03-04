from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from orders_service.application.use_cases import OrderService
from orders_service.infrastructure.repository import SQLAlchemyOrderRepository

# ---- JWT CONFIG ----
SECRET_KEY = "mi-clave-secreta"
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["sha256_crypt"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# ---- APP ----
app = FastAPI(title="Orders Service")

# Inyección de dependencias
repository = SQLAlchemyOrderRepository()
service = OrderService(repository)

# Usuarios simulados
usuarios_db = {"luis": {"username": "luis", "password": pwd_context.hash("1234")}}


# ---- FUNCIONES JWT ----
def verificar_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)


def crear_token(username: str) -> str:
    return jwt.encode({"sub": username}, SECRET_KEY, algorithm=ALGORITHM)


def obtener_usuario_actual(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido")


# ---- SCHEMAS ----
class CreateOrderRequest(BaseModel):
    customer_id: str


class AddItemRequest(BaseModel):
    product_id: str
    product_name: str
    quantity: int
    unit_price: float


# ---- ENDPOINTS ----
@app.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends()):
    usuario = usuarios_db.get(form.username)
    if not usuario or not verificar_password(form.password, usuario["password"]):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    token = crear_token(form.username)
    return {"access_token": token, "token_type": "bearer"}


@app.post("/orders")
def create_order(
    request: CreateOrderRequest, usuario: str = Depends(obtener_usuario_actual)
):
    order = service.create_order(request.customer_id)
    return {
        "id": order.id,
        "customer_id": order.customer_id,
        "status": order.status.value,
    }


@app.get("/orders")
def get_all_orders(usuario: str = Depends(obtener_usuario_actual)):
    orders = service.get_all_orders()
    return [
        {
            "id": o.id,
            "customer_id": o.customer_id,
            "status": o.status.value,
            "total": o.total(),
        }
        for o in orders
    ]


@app.get("/orders/{order_id}")
def get_order(order_id: str, usuario: str = Depends(obtener_usuario_actual)):
    try:
        order = service.get_order(order_id)
        return {
            "id": order.id,
            "customer_id": order.customer_id,
            "status": order.status.value,
            "total": order.total(),
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.post("/orders/{order_id}/items")
def add_item(
    order_id: str,
    request: AddItemRequest,
    usuario: str = Depends(obtener_usuario_actual),
):
    try:
        order = service.add_item(
            order_id,
            request.product_id,
            request.product_name,
            request.quantity,
            request.unit_price,
        )
        return {"id": order.id, "total": order.total()}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.post("/orders/{order_id}/confirm")
def confirm_order(order_id: str, usuario: str = Depends(obtener_usuario_actual)):
    try:
        order = service.confirm_order(order_id)
        return {"id": order.id, "status": order.status.value}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
