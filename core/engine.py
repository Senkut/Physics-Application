import pygame
import sys

class Engine:
    def __init__(self, width=1000, height=800, title="Physic Application"):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.runnig = True
        
        # Para saber que escena se esta ejecutando
        self.current_scene = None
    
    
    def chenge_scene(self , new_scene):
        # Metodo para cambiar a otra scena
        self.current_scene = new_scene
    
    def run(self):
        while self.runnig:
            # Obtener los eventos del sistemas
            events = pygame.event.get()
            
            for event in events:
                if event.type == pygame.QUIT:
                    self.runnig = False
            
            # Poner eventos de la escena actual
            if self.current_scene:
                self.current_scene.handle_event(events)
            
            # Calcula el delta time para tener todos los mismos fps
            dt = self.clock.tick(60) / 1000
            
            if self.current_scene:
                self.current_scene.update(dt)
            
            # Dibujamos lo que pongamos en las scenas
            self.screen.fill("black") # Se limpia la pantalla
            if self.current_scene:
                self.current_scene.draw(self.screen)
            
            pygame.display.flip()
            
        pygame.quit()
        sys.exit()