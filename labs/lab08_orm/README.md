# Lab08 - Acceso a Datos y ORM

## Objetivo
Cómo conectar Python a una base de datos con SQLAlchemy y Alembic.

## Conceptos clave
- **SQLAlchemy** - ORM para base de datos, como Entity Framework en C#
- **SessionLocal** - conexión a la DB, como DbContext en C#
- **CRUD** - crear, leer, actualizar y eliminar registros
- **Alembic** - migraciones de base de datos, como EF Migrations en C#
- **alembic upgrade head** - aplica todas las migraciones pendientes   - - --estudiar mas esta parte

## Cómo correrlo
```bash
python main.py
alembic upgrade head
```