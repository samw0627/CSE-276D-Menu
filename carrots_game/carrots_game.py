import pygame
import os
import random
import sys
from pygame import mixer
from pygame.locals import *
from utils import *


pygame.init()
clock = pygame.time.Clock()
_display_surf = pygame.display.set_mode((WIDTH, HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF)

class bunny:
    def __init__(self, speed):
        self.img = pygame.image.load(BUNNY_IMG)
        self.rect = self.img.get_rect()
        self.x_pos = STARTING_POS_X_BUNNY
        self.y_pos = STARTING_POS_Y_BUNNY
        self.speed = speed
        
    def move(self, direction):
        if direction == RIGHT:
            self.x_pos += self.speed
        else:
            self.x_pos -= self.speed
        self.rect.topleft = (self.x_pos, self.y_pos)
            
    def checkBorder(self):
        if self.x_pos < 0:
            self.x_pos = 0
        if self.x_pos > (WIDTH-BUNNY_SIZE*2):
            self.x_pos = WIDTH-BUNNY_SIZE*2
        
    def draw(self, screen):
        screen.blit(self.img, (self.x_pos, self.y_pos))

class meteor:
    def __init__(self, speed):
        self.speed = speed
        self.img = pygame.image.load(METEOR_IMG)
        self.rect = self.img.get_rect()
        self.x_pos = random.randint(0,WIDTH-METEOR_SIZE*2)
        self.y_pos = STARTING_POS_Y_METEOR
    
    def checkBorder(self):
        if self.y_pos > GROUND_POS_Y:
            self.reset()
    
    def reset(self):
        self.y_pos = 0
        self.x_pos = random.randint(0,WIDTH-METEOR_SIZE*2)
        
    def drop(self):
        self.y_pos += self.speed
        self.rect.topleft = (self.x_pos, self.y_pos)
    
    def draw(self, screen):
        screen.blit(self.img, (self.x_pos, self.y_pos))    
    
    
class carrot:
    def __init__(self, speed):
        self.speed = speed
        self.img = pygame.image.load(CARROT_IMG)
        self.rect = self.img.get_rect()
        self.x_pos = random.randint(0,WIDTH-CARROT_SIZE*2)
        self.y_pos = STARTING_POS_Y_CARROT
    
    def checkBorder(self):
        if self.y_pos > GROUND_POS_Y:
            self.reset()
    
    def reset(self):
        self.y_pos = 0
        self.x_pos = random.randint(0,WIDTH-CARROT_SIZE*2)
        
    def drop(self):
        self.y_pos += self.speed
        self.rect.topleft = (self.x_pos, self.y_pos)
    
    def draw(self, screen):
        screen.blit(self.img, (self.x_pos, self.y_pos))

class score_board:
    def __init__(self):
        self.scores = 0
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        self.img = pygame.image.load(SCORE_BOARD_IMG)
        self.text = None
        self.rect = None
        
    def draw(self, screen):
        text = self.font.render(':' + str(self.scores), True, CARROT_COLOR)
        rect = text.get_rect()
        rect.center = (900, 40)
        screen.blit(text, rect)
        screen.blit(self.img, (860, 20))

class hearts:
    def __init__(self, num_hearts):
        self.num_hearts = num_hearts     
        self.img = pygame.image.load(HEART_IMG)
        
    def draw(self, screen):
        for i in range(self.num_hearts):
            screen.blit(self.img, (STARTING_POS_X_HEART + HEART_SIZE*i, STARTING_POS_Y_HEART))
        
class control:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = WIDTH, HEIGHT
        
        
        
        #set the size of the window 
        self._display_surf = _display_surf
        pygame.display.set_caption(GAME_NAME)
        
        self.background = pygame.image.load(BACKGROUND_IMG)  
        self.bunny = bunny(BUNNY_SPEED)
        self.carrots = [carrot(random.randint(MIN_CARROT_SPEED, MAX_CARROT_SPEED)) for i in range(NUMBER_CARROT)]
        self.carrots_rect = [carrot.rect for carrot in self.carrots]
        self.meteors = [meteor(random.randint(MIN_METEOR_SPEED, MAX_METEOR_SPEED)) for i in range(NUMBER_METEOR)]
        self.meteors_rect = [meteor.rect for meteor in self.meteors]
        self.hearts = hearts(NUM_HEARTS)
        self.score_board = score_board()
        self._mixer = None
        self.points = 0
        
    def on_init(self):
        self._running = True
 
    def on_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            self._running = False
            sys.exit()
            
    def on_loop(self):
        #TODO: replaced by touchPad input later
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.bunny.move(LEFT)
        if keys[pygame.K_RIGHT]:
            self.bunny.move(RIGHT)
        self.bunny.checkBorder()
        for carrot in self.carrots:
            carrot.drop()
            carrot.checkBorder()
            
        for meteor in self.meteors:
            meteor.drop()
            meteor.checkBorder()
        
        collide_idx = self.bunny.rect.collidelist(self.carrots_rect)
        if collide_idx != -1:
            self.score_board.scores += 1
            self.carrots[collide_idx].reset()
        
        collide_idx = self.bunny.rect.collidelist(self.meteors_rect)
        if collide_idx != -1:
            self.hearts.num_hearts -= 1
            self.meteors[collide_idx].reset()

    def on_render(self):
        self._display_surf.blit(self.background, TOP_LEFT)
        self.score_board.draw(self._display_surf)
        for carrot in self.carrots:
            carrot.draw(self._display_surf) 
        for meteor in self.meteors:
            meteor.draw(self._display_surf) 
        self.bunny.draw(self._display_surf)
        self.hearts.draw(self._display_surf)
        pygame.display.flip()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
            
        while(self._running):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
            clock.tick(FPS)
            #Reset the game after all the hearts running out
            if self.hearts.num_hearts == 0:
                self._running = False
        
        show_menu(0,self.score_board.scores)    

def show_menu(num_hearts,scores):
    running = True
    # _display_surf = pygame.display.set_mode((WIDTH, HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF)
    while running:
        
        _display_surf.fill(MENU_BACKGROUND)
        font = pygame.font.Font('freesansbold.ttf', 30)
        
        if num_hearts == 0:
            text = font.render("Press any Key to Restart", True, (0, 0, 0))
            score = font.render("Your Score: " + str(scores), True, (0, 0, 0))
            scoreRect = score.get_rect()
            scoreRect.center = (WIDTH // 2, HEIGHT // 2 + 50)
            _display_surf.blit(score, scoreRect)
            
            
        else:
            _display_surf.fill((135, 206, 235))
            text = font.render("Press any Key to Start", True, (0, 0, 0))
        
        textRect = text.get_rect()
        textRect.center = (WIDTH // 2, HEIGHT // 2)
        _display_surf.blit(text, textRect)
        _display_surf.blit(pygame.image.load(BUNNY_IMG), (WIDTH // 2 - 20, HEIGHT // 2 - 140))
        pygame.display.update()
        #Add delay for displaying the score 
        pygame.time.wait(DISPLAY_DURATION)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
            elif event.type == pygame.KEYDOWN:
                _control = control()
                _control.on_execute()    
        clock.tick(FPS)
        
    pygame.quit()
    sys.exit()
                
if __name__ == "__main__" :
    show_menu(NUM_HEARTS, 0)  