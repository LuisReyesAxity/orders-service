import json
import csv
import logging
from pathlib import Path
from datetime import datetime


# ---- LOGGING - como ILogger en C# ----
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ---- DATETIME ----
ahora = datetime.now()
print(f"Fecha actual: {ahora.strftime('%Y-%m-%d')}")
logger.info("Programa iniciado")


# ---- PATHLIB - crear carpeta y archivo ----
carpeta = Path("datos")
carpeta.mkdir(exist_ok=True)


# ---- JSON - escribir y leer ----
ordenes = [
    {"id": "1", "cliente": "Luis", "total": 150.0},
    {"id": "2", "cliente": "Ana", "total": 80.0},
]

archivo_json = carpeta / "ordenes.json"
with open(archivo_json, "w") as f:
    json.dump(ordenes, f, indent=2)
logger.info("JSON guardado")

with open(archivo_json, "r") as f:
    leidas = json.load(f)
print(f"Órdenes en JSON: {len(leidas)}")


# ---- CSV - escribir y leer ----
archivo_csv = carpeta / "ordenes.csv"
with open(archivo_csv, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["id", "cliente", "total"])
    writer.writeheader()
    writer.writerows(ordenes)
logger.info("CSV guardado")

with open(archivo_csv, "r") as f:
    reader = csv.DictReader(f)
    ordenes_csv = list(reader)
print(f"Órdenes en CSV: {len(ordenes_csv)}")


# ---- MÉTRICAS ----
total = sum(float(o["total"]) for o in ordenes_csv)
print(f"Total ventas: ${total}")