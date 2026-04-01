from core.engine import Engine
from core.scene import Scene

from scenes.caida_libre.caida_scene import CaidaLibreScene

if __name__ == "__main__":
    # Inicializamos el motor
    game_engine = Engine()
    
    # Creamos una scena vacia de prueba (despues se cambia a una real)
    initial_scene = CaidaLibreScene(game_engine)
    game_engine.change_scene(initial_scene)
    
    # Iniamos el game loop
    game_engine.run()