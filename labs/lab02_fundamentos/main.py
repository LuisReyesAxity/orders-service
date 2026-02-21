import json


# ---- TIPOS BÁSICOS ----
# En C#: string, int, bool, float
# En Python es igual pero sin declarar el tipo
nombre = "Orders Service"
version = 1
activo = True
precio = 99.99

print(f"Sistema: {nombre} v{version}")  # f-string = string interpolation de C#


# ---- LISTAS Y DICCIONARIOS ----
# Simulamos órdenes como lista de diccionarios
ordenes = [
    {"id": 1, "cliente": "Luis", "total": 150.0, "status": "pending"},
    {"id": 2, "cliente": "Ana",  "total": 80.0,  "status": "confirmed"},
    {"id": 3, "cliente": "Juan", "total": 200.0, "status": "pending"},
    {"id": 4, "cliente": "Maria","total": 50.0,  "status": "cancelled"},
]


# ---- CONTROL DE FLUJO ----
# Filtrar solo las órdenes pendientes
pendientes = []
for orden in ordenes:
    if orden["status"] == "pending":
        pendientes.append(orden)

print(f"\nÓrdenes pendientes: {len(pendientes)}")


# ---- COMPRENSIONES (pythonic) ----
# Lo mismo pero en una línea — equivale a LINQ en C#
confirmadas = [o for o in ordenes if o["status"] == "confirmed"]
print(f"Órdenes confirmadas: {len(confirmadas)}")


# ---- AGREGACIÓN ----
total_pendiente = sum(o["total"] for o in pendientes)
print(f"Total pendiente: ${total_pendiente}")


# ---- MANEJO DE ERRORES ----
# Simula leer un archivo JSON
def cargar_ordenes(ruta: str) -> list:
    try:
        with open(ruta, "r") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        print(f"Error: archivo '{ruta}' no encontrado")
        return []
    except json.JSONDecodeError:
        print("Error: el archivo no tiene formato JSON válido")
        return []


# Prueba con archivo que no existe,
resultado = cargar_ordenes("ordenes.json")
print(f"\nÓrdenes desde archivo: {resultado}")

# despues de esto ya existe ya lo aghregue entonces ya nop hay errores, LRL

# ---- PATTERN MATCHING (switch de C#) ----
def describir_status(status: str) -> str:
    match status:
        case "pending":
            return "Pendiente de confirmación"
        case "confirmed":
            return "Confirmada"
        case "cancelled":
            return "Cancelada"
        case _:
            return "Status desconocido"


for orden in ordenes:
    print(f"Orden {orden['id']}: {describir_status(orden['status'])}")