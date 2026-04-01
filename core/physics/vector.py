class Vector2:
    def __init__(self, x= 0 , y =0):
        self.x = x
        self.y = y
    
    # Para sumar vectores: v1 + v2
    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)
    
    # Para multiplicar un vector por un numero 
    def __mul__(self, scalar):
        return Vector2(self.x * scalar.x, self.y * scalar.y)
    
    # Tuplas pa dibujar los vectores porque tuplas porque asi lo necesita pygame
    def to_tuple(self):
        return (int(self.x), int(self.y))