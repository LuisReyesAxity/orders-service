import logging
import httpx

# ---- CONFIGURACIÓN INICIAL ----
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Esta es nuestra URL base (como el BaseAddress en un HttpClient)
URL = "https://jsonplaceholder.typicode.com"


# ---- GET - Obtener un recurso (Como GetAsync) ----
print("--- GET ---")
# httpx.get hace la petición síncrona. 
response = httpx.get(f"{URL}/posts/1")
print(f"Status: {response.status_code}")

# .json() es el equivalente a Deserialize<T>(). Convierte el cuerpo en un diccionario.
data = response.json()
print(f"Título: {data['title']}")
logger.info("Post obtenido correctamente")


# ---- GET con timeout (Evitar que el hilo se bloquee para siempre) ----
print("\n--- GET con timeout ---")
try:
    # timeout=5.0 es como establecer client.Timeout en .NET.
    response = httpx.get(f"{URL}/posts", timeout=5.0)
    posts = response.json()
    print(f"Posts obtenidos: {len(posts)}")
except httpx.TimeoutException:
    # Captura específica si el servidor no responde a tiempo.
    print("La petición tardó demasiado")


# ---- Manejo de errores (HTTP Status Codes) ----
print("\n--- Manejo de errores ---")
response = httpx.get(f"{URL}/posts/9999")
# En C# usarías response.IsSuccessStatusCode; aquí validamos el código directo.
if response.status_code == 404:
    print("Post no encontrado (404)")
else:
    print(f"Status: {response.status_code}")


# ---- REINTENTOS ----
print("\n--- Reintentos ---")
# Un bucle for simple para reintentar la conexión si falla (como una mini-librería Polly).
for intento in range(1, 4):
    try:
        response = httpx.get(f"{URL}/posts/1", timeout=5.0)
        print(f"Éxito en intento {intento}")
        break # Si funciona, salimos del bucle.
    except Exception as e:
        print(f"Intento {intento} fallido: {e}")


# ---- STREAMING - Descarga por trozos (Eficiencia de Memoria) ----
print("\n--- Streaming ---")
# 'with httpx.stream' es vital para archivos grandes. 
# En lugar de cargar todo el JSON de 50MB en RAM, lo lee por "pedazos" (chunks).
with httpx.stream("GET", f"{URL}/photos") as response:
    # "wb" significa Write Binary (Escribir en binario).
    with open("fotos.json", "wb") as archivo:
        # iter_bytes() va pidiendo datos al servidor poco a poco.
        for chunk in response.iter_bytes():
            archivo.write(chunk)
print("Archivo guardado en disco sin saturar la RAM")