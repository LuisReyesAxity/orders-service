import time
import random
from contextlib import contextmanager


# ---- FUNCIONES BÁSICAS ----
def crear_orden(cliente: str, *productos, **opciones):
    print(f"Cliente: {cliente}")
    print(f"Productos: {productos}")
    print(f"Opciones: {opciones}")


crear_orden("Luis", "Widget", "Gadget", urgente=True, descuento=10)


# ---- DECORADOR SIMPLE DE REINTENTOS ----
def reintentar(func):
    def wrapper(*args, **kwargs):
        for intento in range(1, 4):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f"Intento {intento} fallido: {e}")
        print("Falló después de 3 intentos")
    return wrapper


@reintentar
def llamar_api():
    if random.random() < 0.7:
        raise ConnectionError("API no disponible")
    return "Respuesta exitosa"


print("\n--- Decorador de reintentos ---")
resultado = llamar_api()
if resultado:
    print(f"Resultado: {resultado}")


# ---- GENERADOR POR LOTES ----
def lotes(lista: list, tamanio: int):
    for i in range(0, len(lista), tamanio):
        yield lista[i:i + tamanio]


ordenes = list(range(1, 11))

print("\n--- Generador por lotes ---")
for lote in lotes(ordenes, 3):
    print(f"Lote: {lote}")


# ---- CONTEXT MANAGER DE TEMPORIZACIÓN ----
@contextmanager
def temporizar(nombre: str):
    inicio = time.time()
    print(f"\nIniciando: {nombre}")
    try:
        yield
    finally:
        fin = time.time()
        print(f"{nombre} tardó: {fin - inicio:.4f} segundos")


print("\n--- Context manager de temporización ---")
with temporizar("Procesar órdenes"):
    time.sleep(0.5)
    print("Procesando...")


'''
# En vez de hacer esto:
def doble(x):
    return x * 2

# Haces esto en una línea:
doble = lambda x: x * 2


contar = contador(0)
contar()  # recuerda: 1
contar()  # recuerda: 2
contar()  # recuerda: 3

'''