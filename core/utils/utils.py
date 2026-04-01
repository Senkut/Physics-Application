from core.constants import *

# Convierete metros a pixeles tambien invierte el eje Y
# Recibe un vecto2 y devuelve una tupla de pixeles
def world_to_screen(world_pos_vector):
    screen_x = world_to_screen.x * PPM
    
    screen_y = HEIGHT - (world_pos_vector.y * PPM)
    
    return (int(screen_x), int(screen_y))