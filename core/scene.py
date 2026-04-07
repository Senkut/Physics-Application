from abc import ABC, abstractmethod
class Scene(ABC):

    def __init__(self, engine):
        # Le pasamos el engine a la escena para que la escena pueda
        # acceder a la pantalla o decirle al motor "cambia a otra escena"
        self.engine = engine
    
    # Lee las teclas los clicks de mouse y diferentes entradas\
    @abstractmethod
    def handle_event(self, event):
        pass
    
    # Actualiza la logica como matematicas posiciones de cosas etc
    @abstractmethod
    def update(self, dt):
        pass
    
    # Dibuja en pantalla lo que se ponga
    @abstractmethod
    def draw(self, screen):
        pass