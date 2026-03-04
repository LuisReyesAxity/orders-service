from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext
from pydantic import BaseModel

# ---- CONFIGURACIÓN (Como el appsettings.json) ----
# Esta clave es la "firma" de tus tokens. ¡No se la des a nadie!
SECRET_KEY = "mi-clave-secreta"
ALGORITHM = "HS256"

# ---- CONTRASEÑAS (Como el PasswordHasher) ----
# Sirve para convertir "1234" en algo ilegible como "as89d7as98d7"
pwd_context = CryptContext(schemes=["sha256_crypt"])

# ---- EL PORTERO (OAuth2) ----
# Le dice a FastAPI: "Busca un token en el botón de Authorize o en los Headers"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

app = FastAPI(title="Orders API con JWT")


# ---- BASE DE DATOS DE MENTIRA (En memoria) ----
# Un diccionario donde guardamos al usuario 'luis' con su clave ya encriptada.
usuarios_db = {"luis": {"username": "luis", "password": pwd_context.hash("1234")}}


# ---- HERRAMIENTAS DE SEGURIDAD ----

def verificar_password(password: str, password_hash: str) -> bool:
    """ Compara la clave que envían con la que tenemos guardada. """
    return pwd_context.verify(password, password_hash)

def crear_token(username: str) -> str:
    """ Crea el 'ticket de entrada' (JWT) para el usuario. """
    return jwt.encode({"sub": username}, SECRET_KEY, algorithm=ALGORITHM)

def obtener_usuario_actual(token: str = Depends(oauth2_scheme)) -> str:
    """ 
    Esta es la pieza más importante. 
    Se asegura de que el token sea válido antes de dejarte entrar a un endpoint.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except Exception:
        # Si el token es falso o viejo, lanzamos error 401 (No tienes permiso).
        raise HTTPException(status_code=401, detail="Token inválido")


# ---- MODELOS DE DATOS (Como tus Clases DTO) ----
class OrderRequest(BaseModel):
    customer_id: str


# ---- RUTA PARA LOGUEARSE (Login) ----
@app.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends()):
    # 1. Buscamos si el usuario existe
    usuario = usuarios_db.get(form.username)
    # 2. Si no existe o la clave está mal, error.
    if not usuario or not verificar_password(form.password, usuario["password"]):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    
    # 3. Si todo ok, le damos su token.
    token = crear_token(form.username)
    return {"access_token": token, "token_type": "bearer"}


# ---- RUTAS PROTEGIDAS (Solo entras con Token) ----

@app.get("/orders")
def get_orders(usuario: str = Depends(obtener_usuario_actual)):
    # Al poner 'Depends(obtener_usuario_actual)', FastAPI corre esa función primero.
    return {"message": f"Hola {usuario}, aquí están tus órdenes"}


@app.post("/orders")
def create_order(request: OrderRequest, usuario: str = Depends(obtener_usuario_actual)):
    # Aquí recibimos el JSON (OrderRequest) y el usuario validado.
    return {
        "message": f"Orden creada por {usuario}",
        "customer_id": request.customer_id,
    }