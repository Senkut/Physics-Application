from core.scene import Scene
from core.constants import *
import pygame

class CaidaLibreScene(Scene):
    def __init__(self, engine):
        super().__init__(engine)
        
        # Posicion en metros
        self.y = 10 # Altura inicial
        self.v = 0 # Velocidad
        self.g = GRAVITY # Gravedad
        # dt es el tiempo
        
        
    def update(self, dt):
        
        # Aplicamos la formula v = v + g*t
        self.v += self.g * dt
        
        # la otra formula y = y + v*t
        self.y -= self.v * dt # negativo porque cae
        
        # Para que no atrviese el piso
        if self.y <= 0:
            self.y =0
            self.v = 0
        
    def draw(self, screen):
        screen.fill(DARK_GRAY)
        
        # Convierte metros a pixeles
        x = WIDTH // 2
        y_pixel = HEIGHT - int(self.y * PPM)
        
        pygame.draw.circle(screen, (RED), ( x, y_pixel), 20)