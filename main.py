import pygame

pygame.init()

screen = pygame.display.set_mode((1000,800))
clock = pygame.time.Clock()
runnig = True
delta_time = 0 #Tiempo que paso desde el ultimo frame(sirve para que sin importar los fps se muevan igual no mas rapido no mas lento)

#Crea un vector2(2d) en el centro exacto de la pantalla
#Lo guarda como posicion del jugador
player_position = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

while runnig:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runnig = False
    screen.fill("red")
    
    #Crea un poligono(Triangulo)
    pygame.draw.polygon(screen,"white",[
        (player_position.x      ,player_position.y - 50), 
        (player_position.x - 50 ,player_position.y + 50), 
        (player_position.x + 50 ,player_position.y + 50)
        ], 0)
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_position.y -= 300 * delta_time
    if keys[pygame.K_s]:
        player_position.y += 300 * delta_time
    if keys[pygame.K_a]:
        player_position.x -= 300 * delta_time
    if keys[pygame.K_d]:
        player_position.x += 300 * delta_time
    
    #Actualiza lo que pase en pantalla
    pygame.display.flip()
    
    delta_time = clock.tick(60) / 1000
    
pygame.quit()