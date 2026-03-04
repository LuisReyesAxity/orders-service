# Declaración de variables
x = 1
y = 2

#Definicón de función
def suma(a, b):
    return a + b

# CONSTRUCTOR: Se ejecuta automaticamente al crear el objeto.
    # 'self' es como 'this' en C#: permite acceder a los datos internos.
class miClase:
    def __init__(self, nombre):
        self.nombre = nombre
        
# METODO DE INSTANCIA: Una accion que el objeto puede realizar.
    # Siempre debe recibir 'self' para poder leer sus propios atributos.
    def saludar(self):
        print("Hola " + self.nombre)
