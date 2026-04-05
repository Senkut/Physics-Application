from core.constants import *
import pygame
import sys

class Engine:
    def __init__(self, title="Physic Application"):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.running = True
        self.fullscreen = False
        
        # Para saber que escena se esta ejecutando
        self.current_scene = None
    
    def change_scene(self , new_scene):
        # Metodo para cambiar a otra scena
        self.current_scene = new_scene
    
    def run(self):
        while self.running:
            # Obtener los eventos del sistemas
            events = pygame.event.get()
            
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
            
            # Poner en modo ventana o pantalla completa
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11:
                        self.fullscreen = not self.fullscreen
                        if self.fullscreen:
                            self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
                        else:
                            self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
                
            # Poner eventos de la escena actual
            if self.current_scene:
                self.current_scene.handle_event(events)
            
            # Calcula el delta time para tener todos los mismos fps
            dt = self.clock.tick(60) / 1000
            
            if self.current_scene:
                self.current_scene.update(dt)
            
            # Dibujamos lo que pongamos en las scenas
            self.screen.fill(DARK_GRAY) # Se limpia la pantalla
            if self.current_scene:
                self.current_scene.draw(self.screen)
            
            pygame.display.flip()

        pygame.quit()
        sys.exit()