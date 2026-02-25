from typing import Optional, Union


# ---- TIPO EN FUNCIONES ----
# Sin tipo - Python lo permite pero no es buena práctica
def saludar(nombre):
    return "Hola " + nombre

# Con tipo - como C#, más claro
def saludar_tipado(nombre: str) -> str:
    return "Hola " + nombre

print(saludar_tipado("Luis"))


# ---- OPTIONAL - puede ser None ----
# Como string? en C# (nullable)
def buscar_orden(id: str) -> Optional[str]:
    ordenes = {"1": "Orden de Luis", "2": "Orden de Ana"}
    return ordenes.get(id)

print("\n--- Optional ---")
print(buscar_orden("1"))   # encuentra la orden
print(buscar_orden("99"))  # retorna None


# ---- UNION - acepta dos tipos ----
# Como object en C# pero más específico
def procesar(valor: Union[int, str]) -> str:
    if isinstance(valor, int):
        return f"Es un número: {valor}"
    return f"Es texto: {valor}"

print("\n--- Union ---")
print(procesar(42))
print(procesar("hola"))


# ---- LISTAS TIPADAS ----
# Como List<int> en C#
def filtrar_mayores(numeros: list[int], minimo: int) -> list[int]:
    return [n for n in numeros if n >= minimo]

print("\n--- Lista tipada ---")
print(filtrar_mayores([1, 5, 3, 8, 2], 4))

# ---- ERROR DE TIPOS - mypy lo detecta ----
def sumar(a: int, b: int) -> int:
    return a + b

# Esto está mal - mandamos string en vez de int
resultado = sumar("hola", 2)
print(resultado)