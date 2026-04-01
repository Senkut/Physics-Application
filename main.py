from core.engine import Engine
from core.scene import Scene

if __name__ == "__main__":
    # Inicializamos el motor
    game_engine = Engine()
    
    # Creamos una scena vacia de prueba (depues se cambia a una real)
    initial_scene = Scene(game_engine)
    game_engine.chenge_scene(initial_scene)
    
    # Iniamos el game loop
    game_engine.run()