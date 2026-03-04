from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext
from pydantic import BaseModel

# Configuración JWT
SECRET_KEY = "mi-clave-secreta"
ALGORITHM = "HS256"

# Para encriptar contraseñas - como BCrypt en C#
pwd_context = CryptContext(schemes=["sha256_crypt"])

# Esquema de seguridad
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

app = FastAPI(title="Orders API con JWT")


# ---- USUARIOS - simulados en memoria ----
# En producción estarían en la DB
usuarios_db = {"luis": {"username": "luis", "password": pwd_context.hash("1234")}}


# ---- FUNCIONES DE AUTENTICACIÓN ----
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


class OrderRequest(BaseModel):
    customer_id: str


# ---- ENDPOINTS ----
@app.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends()):
    usuario = usuarios_db.get(form.username)
    if not usuario or not verificar_password(form.password, usuario["password"]):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    token = crear_token(form.username)
    return {"access_token": token, "token_type": "bearer"}


@app.get("/orders")
def get_orders(usuario: str = Depends(obtener_usuario_actual)):
    return {"message": f"Hola {usuario}, aquí están tus órdenes"}


@app.post("/orders")
def create_order(request: OrderRequest, usuario: str = Depends(obtener_usuario_actual)):
    return {
        "message": f"Orden creada por {usuario}",
        "customer_id": request.customer_id,
    }
