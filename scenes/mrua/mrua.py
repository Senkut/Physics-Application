import pygame
import pygame.math as vc
import pygame.image as spr
from core.engine import Engine
from core.constants import WIDTH,HEIGHT
from core.scene import Scene
from core.physics.formulas import * 
class Mrua(Scene):
    def __init__(self, vel, acel,path_image =r"image\download.jpg"):
        self.sprite =  spr.load(path_image).convert_alpha()
        self.engine = Engine("mru")
        self.potion = vc.Vector2(WIDTH/2,HEIGHT/2)
        self.velocity = vel
        self.aceleration = acel
    def handle_event(self, event):
        print("poner los eventos que use para cojer los datos de usrer")
    def update(self, dt): #el dt = self.engine.clock.tick(60)/1000.0
        self.mov(dt)
    def draw(self, screen):
        screen.blit(self.sprite,self.potion)
    def run():
        print("malaver como dijimos implemento yo logica tu implementa solo que se mueva y se vea bien")
    def mov(self,dt):
        self.potion.x = mrua_pos(self.potion[0],self.velocity,self.aceleration,dt)
        self.velocity += self.aceleration*dt