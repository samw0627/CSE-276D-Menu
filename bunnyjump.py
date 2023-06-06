import pygame
import os
import random
import sys
from buttons import menuButton
import menu as mainMenu

pygame.init()

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1024
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

RUNNING = [pygame.image.load(os.path.join("bunnyjump_assets/bunny", "Bunny.png")),
           pygame.image.load(os.path.join("bunnyjump_assets/bunny", "BunnyRun1.png")),
           pygame.image.load(os.path.join("bunnyjump_assets/bunny", "BunnyRun2.png"))] 

JUMPING = pygame.image.load(os.path.join("bunnyjump_assets/bunny", "BunnyRun2.png"))

SNAKE = pygame.image.load(os.path.join("bunnyjump_assets/snake", "Snake.png"))

CLOUD = pygame.image.load(os.path.join("bunnyjump_assets/background", "Cloud.png"))

BG = [pygame.image.load(os.path.join("bunnyjump_assets/background", "Grass.png")), 
      pygame.image.load(os.path.join("bunnyjump_assets/background", "Ground.png")),
      pygame.image.load(os.path.join("bunnyjump_assets/background", "Sky.png"))]

JUMP_SOUND = pygame.mixer.Sound("bunnyjump_assets/jump.wav")

class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(1000, 1200)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()
    
    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(1500, 2000)
            self.y = random.randint(50, 100)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

class Snake:
    def __init__(self):
        self.image = SNAKE
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = 318
    
    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Bunny:
    X_POS = 30
    Y_POS = 316
    JUMP_VEL = 8.5

    def __init__(self):
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.bunny_run = True
        self.bunny_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.bunny_rect  = self.image.get_rect()
        self.bunny_rect.x = self.X_POS
        self.bunny_rect.y = self.Y_POS
    
    def update(self, userInput):
        if self.bunny_run:
            self.run()
        if self.bunny_jump:
            self.jump()
        
        if self.step_index >= 15: # double check this
            self.step_index = 0
        
        if userInput[0] and not self.bunny_jump:
            pygame.mixer.Sound.play(JUMP_SOUND)
            pygame.mixer.music.stop()
            self.bunny_run = False
            self.bunny_jump = True
        elif not (self.bunny_jump or userInput[0]):
            self.bunny_run = True
            self.bunny_jump = False
    
    def run(self):
      self.image = self.run_img[self.step_index // 5]
      self.bunny_rect = self.image.get_rect()
      self.bunny_rect.x = self.X_POS
      self.bunny_rect.y = self.Y_POS
      self.step_index += 1
    
    def jump(self):
        self.image = self.jump_img
        if self.bunny_jump:
            self.bunny_rect.y -= self.jump_vel * 3
            self.jump_vel -= 0.849
        if self.jump_vel < -self.JUMP_VEL:
            self.bunny_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, screen):
      screen.blit(self.image, (self.bunny_rect.x, self.bunny_rect.y))

def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    run = True
    clock = pygame.time.Clock()
    player = Bunny()
    cloud = Cloud()
    game_speed = 10
    x_pos_bg = 0
    y_pos_bg = 348
    points = 0
    font = pygame.font.Font('freesansbold.ttf', 20)
    obstacles = []
    death_count = 0

    # create menu button object
    menuButtonObj = menuButton("test_hamburg_menu.png")

    def score():
        global points, game_speed
        points += 1
        if points % 500 == 0:
            game_speed += 1

        text = font.render("Points: " + str(points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (900, 40)
        SCREEN.blit(text, textRect)

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG[0].get_width()
        for i in range(0, 60):
            SCREEN.blit(BG[0], (image_width*i + x_pos_bg, y_pos_bg))
            for j in range(1, 14):
                SCREEN.blit(BG[1], (image_width*i + x_pos_bg, image_width*j + y_pos_bg))
        if x_pos_bg <= -image_width:
            # SCREEN.blit(BG[0], (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos  # gets mouse position
                if menuButtonObj.button.collidepoint(mouse_pos):
					# jump back to main menu
                    mainMenu.main()
        
        SCREEN.fill((135, 206, 235))
        userInput = pygame.mouse.get_pressed()
        player.draw(SCREEN)
        player.update(userInput)

        if len(obstacles) == 0:
            obstacles.append(Snake())
        
        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.bunny_rect.colliderect(obstacle.rect):
                # pygame.draw.rect(SCREEN, (255, 0, 0), player.bunny_rect, 2)
                pygame.time.delay(1000)
                death_count += 1
                menu(death_count)

        background()
        cloud.draw(SCREEN)
        cloud.update()
        score()

        clock.tick(30)
        SCREEN.blit(menuButtonObj.img, menuButtonObj.img.get_rect(center = menuButtonObj.button.center))
        pygame.display.update()

def menu(death_count):
    global points
    run = True
    # create menu button object
    menuButtonObj = menuButton("test_hamburg_menu.png")
    
    while run:
        SCREEN.fill((135, 206, 235))
        font = pygame.font.Font('freesansbold.ttf', 30)

        if death_count == 0:
            text = font.render("Press screen to Start", True, (0, 0, 0))
        else:
            text = font.render("Press screen to Restart", True, (0, 0, 0))
            score = font.render("Your Score: " + str(points), True, (0, 0, 0))
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(score, scoreRect)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, textRect)
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))
        SCREEN.blit(menuButtonObj.img, menuButtonObj.img.get_rect(center = menuButtonObj.button.center))

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sys.exit()
            # if event.type == pygame.KEYDOWN:
            #     main()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos 
                if menuButtonObj.button.collidepoint(mouse_pos):
                    # jump back to main menu
                    mainMenu.main()
                else:
                    main()
                
# menu(death_count=0)