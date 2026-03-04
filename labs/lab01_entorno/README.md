# Lab01 - Entorno y Herramientas

## Objetivo
Configurar un proyecto Python con las herramientas de calidad de código.

## Herramientas instaladas
- **black** - formatea el código automáticamente
- **isort** - ordena los imports
- **ruff** - detecta errores de calidad
- **pre-commit** - ejecuta todo antes de cada commit

## Cómo correrlo
```bash
black main.py
isort main.py
ruff check main.py
```