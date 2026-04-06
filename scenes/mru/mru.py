import pygame
import pygame.math as vc
import pygame.image as spr
from core.engine import Engine
from core.constants import WHITE,HEIGHT
from core.scene import Scene
from core.physics.formulas import * 
class Mru(Scene):
    def __init__(self,vel=10,path_image = r"image\download.jpg"):
        self.sprite =  spr.load(path_image).convert_alpha()
        self.engine = Engine("mru")
        self.potion = vc.Vector2(WHITE/2,HEIGHT/2)
        self.velocity = vel
    def handle_event(self, event):
        print("poner los eventos que use para cojer los datos de usrer")
    def update(self, dt): #el dt = self.engine.clock.tick(60)/1000.0
        self.mov(dt)
    def draw(self, screen):
        screen.blit(self.sprite,self.potion)
    def run():
        print("malaver como dijimos implemento yo logica tu implementa solo que se mueva y se vea bien")
    def mov(self,dt):
        self.potion.x =mru_pos(self.potion[0],self.velocity,dt)