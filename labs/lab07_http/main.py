import httpx
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API de prueba gratuita - como HttpClient en C#
URL = "https://jsonplaceholder.typicode.com"


# ---- GET - obtener un post ----
print("--- GET ---")
response = httpx.get(f"{URL}/posts/1")
print(f"Status: {response.status_code}")
data = response.json()
print(f"Título: {data['title']}")
logger.info("Post obtenido correctamente")


# ---- GET con timeout ----
print("\n--- GET con timeout ---")
try:
    response = httpx.get(f"{URL}/posts", timeout=5.0)
    posts = response.json()
    print(f"Posts obtenidos: {len(posts)}")
except httpx.TimeoutException:
    print("La petición tardó demasiado")


# ---- Manejo de errores ----
print("\n--- Manejo de errores ---")
response = httpx.get(f"{URL}/posts/9999")
if response.status_code == 404:
    print("Post no encontrado")
else:
    print(f"Status: {response.status_code}")


    # ---- REINTENTOS ----
print("\n--- Reintentos ---")
for intento in range(1, 4):
    try:
        response = httpx.get(f"{URL}/posts/1", timeout=5.0)
        print(f"Éxito en intento {intento}")
        break
    except Exception as e:
        print(f"Intento {intento} fallido: {e}")


# ---- STREAMING - descarga en pedazos ----
print("\n--- Streaming ---")
with httpx.stream("GET", f"{URL}/photos") as response:
    with open("fotos.json", "wb") as archivo:
        for chunk in response.iter_bytes():
            archivo.write(chunk)
print("Archivo guardado en disco")