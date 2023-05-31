import pygame
import os
import random
import sys
from pygame import mixer
from pygame.locals import *
from utils import *

class bunny:
    
    def __init__(self):
        self.img = pygame.image.load(BUNNY_IMG)
        self.x_pos = STARTING_POS_X_BUNNY
        self.y_pos = STARTING_POS_Y_BUNNY
        
    def draw(self, screen):
        screen.blit(self.img, (self.x_pos, self.y_pos))

class carrot:
    def __init__(self, speed):
        self.speed = speed
        self.img = pygame.image.load(CARROT_IMG)
        self.x_pos = random.randint(0,WIDTH)
        self.y_pos = STARTING_POS_Y_CARROT
    def draw(self, screen):
        screen.blit(self.img, (self.x_pos, self.y_pos))

class ground:
    def __init__(self):
        pass
    
BACKGROUND = pygame.image.load(BACKGROUND_IMG)   

class control:
    def __init__(self):
        self._running = True
        self._display_surf = None
        
        self.size = self.width, self.height = WIDTH, HEIGHT
    
        self._clock = pygame.time.Clock()
        
        self.speed = 5
        self.bunny = bunny()
        self.carrot = carrot(self.speed)
        
        self._mixer = None
        
        
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        
        self._display_surf.blit(BACKGROUND, TOP_LEFT)
        self.bunny.draw(self._display_surf)
        self.carrot.draw(self._display_surf)
        self._running = True
 
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
            
    def on_loop(self):
        self.carrot.y_pos += self.carrot.speed
        self.carrot.draw(self._display_surf)
        pygame.display.flip()
    
    def on_render(self):
        pass
    
    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):
            self._clock.tick(FPS)
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()
        
if __name__ == "__main__" :
    control = control()
    control.on_execute()    