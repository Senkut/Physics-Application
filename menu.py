import pygame
import sys
P=1.2
C_D = 0.47
SCALEE = 0.0001
WHITE =(144,213,255)
SIZE = (1400,1200)


def start():


    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(SIZE)

    img = pygame.image.load("image/download.jpg").convert_alpha()
    rect = img.get_rect()
    rect.x = 50


def movMRU(vel, initial_time, current_time, dt, wind, time, mass, a):
    if (current_time - initial_time) < time:
        v_rel = vel - wind
        f_drag = -0.5 * P * C_D * a * v_rel * abs(v_rel)
        accel = f_drag / mass
        vel += accel * dt
        if wind < 0 and vel < wind: vel = wind
        if wind > 0 and vel > wind: vel = wind
            
    return vel

def movMRUA(acl,vel,initial_time,current_time,dt,wind,time,a,mass):
    if (current_time-initial_time)<time:
        velRelative = vel -wind
        netown = -(0.5*P*C_D*a*(velRelative*abs(velRelative)))
        acl_total = acl + (netown/mass)
        vel+= acl_total*dt
    return vel
