# Orders Service

API para gestionar órdenes de compra, construida con Python y arquitectura hexagonal.

## ¿Qué hace?
Permite crear órdenes, agregar productos y confirmarlas. Tiene login con JWT para seguridad.

## Tecnologías usadas
- **FastAPI** - para crear la API (como ASP.NET Core en C#)
- **SQLAlchemy** - para guardar datos en base de datos (como Entity Framework en C#)
- **Pydantic** - para validar datos de entrada
- **JWT** - para autenticación y seguridad
- **pytest** - para pruebas unitarias
- **Docker** - para empaquetar la aplicación

## Arquitectura Hexagonal
El proyecto está dividido en 3 capas:
- **domain** - las reglas de negocio (Order, OrderItem)
- **application** - los casos de uso (crear orden, confirmar orden)
- **infrastructure** - la API y la base de datos

## Cómo correrlo
```bash
uvicorn main:app --reload
```

Abre http://127.0.0.1:8000/docs para ver los endpoints.

## Cómo correr los tests
```bash
$env:PYTHONPATH="src"; pytest tests/ -v
```

## Seguridad
```bash
pip-audit
```