class Scenes:
    def __init__(self, engine):
        # Le pasamos el engine a la escena para que la escena pueda
        # acceder a la pantalla o decirle al motor "cambia a otra escena"
        self.engine = engine
    
    # Lee las teclas los clicks de mouse y diferentes entradas
    def handle_event(self, event):
        self.event = event
        pass
    
    # Actualiza la logica como matematicas posiciones de cosas etc
    def update(self, dt):
        pass
    
    # Dibuja en pantalla lo que se ponga
    def draw(self, screen):
        pass