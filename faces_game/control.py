from facialExpression import facialExpression
from touchPad import touchPad
from sound import sound
import pygame
from pygame import mixer
from pygame.locals import *
from utils import *

class control:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self._display = None
        self.size = self.width, self.height = WIDTH, HEIGHT
    
        self._count = 0
        self.faces = facialExpression(FACE_IMG_DIR)
        self.touch = touchPad()
        self.sound = sound(SOUND_DIR)
        
        self._face = None
        self.display_face = None
        self.face_count = 0
        self.home_state = True
        
        self._mixer = None
        
        
    def on_init(self):
        pygame.init()
        mixer.init()
        
        self._mixer = mixer.music
        self._mixer.set_volume(1.0)
        
        self._display = pygame.display
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
        
        self.reset_state()  
        
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self._face = self.faces.getSillyFace()
                self._mixer.load(self.sound.getSillySound())
                self._mixer.play(2)
                
            elif event.key == pygame.K_s:
                self._face = self.faces.getCuriousFace() 
                self._mixer.load(self.sound.getCuriousSound())
                self._mixer.play(2)
                
            self.home_state = False 
        
    def on_loop(self):
        #TODO: check for the input from touchPad
        # if self.touch.getState() == HOME:
        #     self.face = self.faces.getHappyFace()
        # elif self.touch.getState() == HEAD:
        #     self.face = self.faces.getCuriousFace()
        # elif self.touch.getState() == EAR:
        #     self.face = self.faces.getSillyFace()
        
        if not self.home_state:
            self._count += 1     
            if self._count == EXPRESSION_DURATION:
                self.home_state = True
                self.reset_state()
                
        self._mixer.queue(self.sound.getSmileSound())
                
    def reset_state(self):
        self._face = self.faces.getHappyFace() 
        self._mixer.load(self.sound.getHappySound())
        self._mixer.play(2)
        self._count = 0
        
        
    #Render the facial expression onto screen
    def on_render(self):
        self.anime_faces()
        self._display_surf.blit(self.display_face, TOP_LEFT)
        self._display.update()
    
    def anime_faces(self):
        if self.face_count > OPEN_DURATION:
            self.display_face = pygame.image.load(self._face[BLINK])
            if self.face_count > OPEN_DURATION + BLINK_DURATION:
                self.face_count = 0
        else:
            self.display_face = pygame.image.load(self._face[OPEN])
        self.face_count += 1
        
    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()
 
if __name__ == "__main__" :
    # faces = facialExpression(FACE_IMG_DIR)
    control = control()
    control.on_execute()



