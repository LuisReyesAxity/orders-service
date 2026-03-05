from fastapi import Depends, FastAPI, HTTPException  # FastAPI - como ASP.NET Core en C#
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm  # Para el login
from jose import jwt  # Para crear y verificar tokens JWT
from passlib.context import CryptContext  # Para encriptar contraseñas
from pydantic import BaseModel  # Para validar datos de entrada

from orders_service.application.use_cases import OrderService  # El servicio de órdenes
from orders_service.infrastructure.repository import SQLAlchemyOrderRepository  # El repositorio


# ---- CONFIGURACIÓN JWT ----
SECRET_KEY = "mi-clave-secreta"  # Clave para firmar el token
ALGORITHM = "HS256"              # Algoritmo de encriptación
pwd_context = CryptContext(schemes=["sha256_crypt"])  # Para encriptar contraseñas
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")  # Esquema de seguridad Bearer Token


# ---- APLICACIÓN FASTAPI ----
app = FastAPI(title="Orders Service")  # Crea la app, genera Swagger automático en /docs

# Inyección de dependencias - como DI en C#
repository = SQLAlchemyOrderRepository()  # Adaptador SQLAlchemy
service = OrderService(repository)        # Servicio recibe el repositorio

# Usuarios simulados en memoria - en producción estarían en la DB
usuarios_db = {"luis": {"username": "luis", "password": pwd_context.hash("1234")}}


# ---- FUNCIONES JWT ----
def verificar_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)  # Compara contraseña con hash


def crear_token(username: str) -> str:
    return jwt.encode({"sub": username}, SECRET_KEY, algorithm=ALGORITHM)  # Crea el token


def obtener_usuario_actual(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  # Verifica el token
        return payload.get("sub")  # Retorna el username del token
    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido")  # Token inválido = 401


# ---- SCHEMAS PYDANTIC ----
# Validan los datos que entran a la API - como Data Annotations en C#
class CreateOrderRequest(BaseModel):
    customer_id: str  # Solo necesita el ID del cliente


class AddItemRequest(BaseModel):
    product_id: str    # ID del producto
    product_name: str  # Nombre del producto
    quantity: int      # Cantidad
    unit_price: float  # Precio unitario


# ---- ENDPOINTS ----
@app.post("/login")  # POST /login - no requiere token
def login(form: OAuth2PasswordRequestForm = Depends()):
    usuario = usuarios_db.get(form.username)
    if not usuario or not verificar_password(form.password, usuario["password"]):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")  # 401 si falla
    token = crear_token(form.username)  # Crea el token
    return {"access_token": token, "token_type": "bearer"}  # Retorna el token


@app.post("/orders")  # POST /orders - requiere token
def create_order(
    request: CreateOrderRequest, usuario: str = Depends(obtener_usuario_actual)  # Verifica token
):
    order = service.create_order(request.customer_id)  # Llama al caso de uso
    return {"id": order.id, "customer_id": order.customer_id, "status": order.status.value}


@app.get("/orders")  # GET /orders - requiere token
def get_all_orders(usuario: str = Depends(obtener_usuario_actual)):
    orders = service.get_all_orders()  # Obtiene todas las órdenes
    return [{"id": o.id, "customer_id": o.customer_id, "status": o.status.value, "total": o.total()} for o in orders]


@app.get("/orders/{order_id}")  # GET /orders/{id} - requiere token
def get_order(order_id: str, usuario: str = Depends(obtener_usuario_actual)):
    try:
        order = service.get_order(order_id)  # Busca la orden por ID
        return {"id": order.id, "customer_id": order.customer_id, "status": order.status.value, "total": order.total()}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))  # 404 si no existe


@app.post("/orders/{order_id}/items")  # POST /orders/{id}/items - requiere token
def add_item(order_id: str, request: AddItemRequest, usuario: str = Depends(obtener_usuario_actual)):
    try:
        order = service.add_item(order_id, request.product_id, request.product_name, request.quantity, request.unit_price)
        return {"id": order.id, "total": order.total()}  # Retorna el total actualizado
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.post("/orders/{order_id}/confirm")  # POST /orders/{id}/confirm - requiere token
def confirm_order(order_id: str, usuario: str = Depends(obtener_usuario_actual)):
    try:
        order = service.confirm_order(order_id)  # Confirma la orden
        return {"id": order.id, "status": order.status.value}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))  # 400 si no se puede confirmar