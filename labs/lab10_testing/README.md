# Lab10 - Pruebas con pytest

## Objetivo
Cómo escribir pruebas unitarias en Python con pytest.

## Conceptos clave
- **pytest** - framework de pruebas, como xUnit en C#
- **assert** - verifica que el resultado es el esperado
- **test_** - cada función que empieza con test_ es una prueba
- **Prueba unitaria** - verifica una sola cosa del dominio

## Pruebas implementadas
- **test_order_total** - verifica que el cálculo del total es correcto
- **test_order_confirm** - verifica que la orden se confirma correctamente
- **test_no_confirmar_dos_veces** - verifica que no se puede confirmar dos veces
- **test_order_cancel** - verifica que la orden se puede cancelar

## Cómo correrlo
```bash
pytest test_orders.py -v
```