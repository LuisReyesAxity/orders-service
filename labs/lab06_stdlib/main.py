import csv
import json
import logging
from datetime import datetime
from pathlib import Path

# ---- LOGGING - como ILogger en C# ----
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ---- DATETIME - Manejo de Fechas ----
ahora = datetime.now()
print(f"Fecha actual: {ahora.strftime('%Y-%m-%d')}")
logger.info("Programa iniciado")


# ---- PATHLIB - Manejo de archivos (Como System.IO.Path)
carpeta = Path("datos")
carpeta.mkdir(exist_ok=True)


# ---- JSON - Serialización (Como System.Text.Json) ----
ordenes = [
    {"id": "1", "cliente": "Luis", "total": 150.0},
    {"id": "2", "cliente": "Ana", "total": 80.0},
]

# Creamos la ruta completa: "datos/ordenes.json".
archivo_json = carpeta / "ordenes.json"

# 'with open' es como el bloque 'using' de C#: cierra el archivo automáticamente al terminar.
# "w" significa Write.
with open(archivo_json, "w") as f:
    json.dump(ordenes, f, indent=2)
logger.info("JSON guardado")

# "r" significa Read.
with open(archivo_json, "r") as f:
    leidas = json.load(f)
print(f"Órdenes en JSON: {len(leidas)}")


# ---- CSV - Lectura y Escritura de Archivos Planos ----
archivo_csv = carpeta / "ordenes.csv"

# newline="" se usa para evitar líneas en blanco extra en Windows.
with open(archivo_csv, "w", newline="") as f:
    # DictWriter nos permite mapear las llaves del diccionario a las columnas del CSV.
    writer = csv.DictWriter(f, fieldnames=["id", "cliente", "total"])
    writer.writeheader()  # Escribe la primera fila con los títulos.
    writer.writerows(ordenes) # Escribe todos los datos.
logger.info("CSV guardado")

with open(archivo_csv, "r") as f:
    # DictReader lee cada fila como si fuera un objeto/diccionario.
    reader = csv.DictReader(f)
    ordenes_csv = list(reader)
print(f"Órdenes en CSV: {len(ordenes_csv)}")


# ---- MÉTRICAS (LINQ en Python) ----
# Esto es una 'List Comprehension'. Es el equivalente a usar .Sum() en LINQ.
# Convertimos o["total"] a float porque en el CSV todo se lee como string.
total = sum(float(o["total"]) for o in ordenes_csv)
print(f"Total ventas: ${total}")