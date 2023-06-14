"""
This file contains the code for the bunny jumping game,
where the user plays as a bunny trying to jump over as many
snakes as possible. Inspiration for this game from 
https://github.com/codewmax/chrome-dinosaur.
"""
import pygame
import os
import random
import sys
from buttons import menuButton
import menu as mainMenu
import RPi.GPIO as GPIO                                      

pygame.init()

# initializing the window size to fit the LCD tablet
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1024
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF)

GPIO.setmode(GPIO.BCM)     # set up BCM GPIO numbering  
GPIO.setup(20, GPIO.IN)    # set GPIO 20 as input

# initializing assets for game animations and sound
RUNNING = [pygame.image.load("bunnyjump_assets/bunny/Bunny.png"),
           pygame.image.load("bunnyjump_assets/bunny/BunnyRun1.png"),
           pygame.image.load("bunnyjump_assets/bunny/BunnyRun2.png")] 

JUMPING = pygame.image.load("bunnyjump_assets/bunny/BunnyRun2.png")

SNAKE = pygame.image.load("bunnyjump_assets/snake/Snake.png")

CLOUD = pygame.image.load(os.path.join("bunnyjump_assets/background", "Cloud.png"))

BG = [pygame.image.load(os.path.join("bunnyjump_assets/background", "Grass.png")), 
      pygame.image.load(os.path.join("bunnyjump_assets/background", "Ground.png")),
      pygame.image.load(os.path.join("bunnyjump_assets/background", "Sky.png"))]

JUMP_SOUND = pygame.mixer.Sound("bunnyjump_assets/jump.wav")

# Class for the cloud object in the background
class Cloud:
    # initializing where the first cloud should be generated
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(1000, 1200)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()
    
    # updating the position of the cloud as the bunny moves across the screen
    def update(self):
        self.x -= game_speed # moving the cloud at the same speed as the game
        if self.x < -self.width: # if the cloud has moved past the end of the screen, reset its position
            self.x = SCREEN_WIDTH + random.randint(1500, 2000)
            self.y = random.randint(50, 100)
    
    # drawing the cloud on the game screen
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

# Class for the snake object that the user will try to jump over 
class Snake:
    # initializing where the first snake should be generated
    def __init__(self):
        self.image = SNAKE
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = 318
    
    # updating the position of the snake as the bunny moves across the screen
    def update(self):
        self.rect.x -= game_speed # moving the snake at the same speed as the game
        if self.rect.x < -self.rect.width: # if the snake has moved past the end of the screen, remove it from the list of snakes
            snakes.pop()
    
    # drawing the snake on the game screen
    def draw(self, screen):
        screen.blit(self.image, self.rect)

# Class for the bunny object that the user will play as
class Bunny:
    X_POS = 30
    Y_POS = 316
    JUMP_VEL = 8.5

    # initializing where the bunny will start from and its instance variables
    def __init__(self):
        self.run_img = RUNNING # the images for when the bunny is running
        self.jump_img = JUMPING # the image for when the bunny is jumping

        self.bunny_run = True
        self.bunny_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL # determines how high the bunny will jump into the air
        self.image = self.run_img[0]
        self.bunny_rect  = self.image.get_rect()
        self.bunny_rect.x = self.X_POS
        self.bunny_rect.y = self.Y_POS
    
    # updating the state of the bunny based on user actions
    def update(self, userInput, fabric):
        if self.bunny_run:
            self.run()
        if self.bunny_jump:
            self.jump()
        
        # check for cycling through the bunny running animations
        if self.step_index >= 15: 
            self.step_index = 0
        
        # if the screen is touched or fabric is touched and the bunny is not already jumping
        if (fabric or userInput[0]) and not self.bunny_jump:
            pygame.mixer.Sound.play(JUMP_SOUND) # play the jumping sound
            pygame.mixer.music.stop()
            self.bunny_run = False
            self.bunny_jump = True
        # if the bunny is not jumping or the screen is not touched or the fabric is not touched, keep running
        elif not (self.bunny_jump or userInput[0] or fabric):
            self.bunny_run = True
            self.bunny_jump = False
    
    # displaying the bunny while it is running
    def run(self):
      self.image = self.run_img[self.step_index // 5] # changing the image for the running animation
      self.bunny_rect = self.image.get_rect()
      self.bunny_rect.x = self.X_POS
      self.bunny_rect.y = self.Y_POS
      self.step_index += 1
    
    # defining the jumping action of the bunny
    def jump(self):
        self.image = self.jump_img
        if self.bunny_jump:
            self.bunny_rect.y -= self.jump_vel * 3 # move the bunny into the air
            self.jump_vel -= 0.849 # decrease the rate at which the bunny is moving into the air
        if self.jump_vel < -self.JUMP_VEL:
            self.bunny_jump = False # making the bunny fall back down from jumping
            self.jump_vel = self.JUMP_VEL # resetting the jump velocity

    # drawing the bunny on the game screen
    def draw(self, screen):
      screen.blit(self.image, (self.bunny_rect.x, self.bunny_rect.y))

def main():
    global game_speed, x_pos_bg, y_pos_bg, points, snakes
    run = True
    clock = pygame.time.Clock()
    player = Bunny() # instance of the bunny the player will play as
    cloud = Cloud() # instance of the cloud moving across the background
    game_speed = 10
    x_pos_bg = 0
    y_pos_bg = 348
    points = 0
    font = pygame.font.Font('freesansbold.ttf', 20)
    snakes = []
    death_count = 0

    # create menu button object
    menuButtonObj = menuButton("test_hamburg_menu.png")

    def score():
        global points, game_speed
        points += 1
        # increase the speed of the game every 500 points
        if points % 500 == 0:
            game_speed += 1

        # displaying the points scored so far in the top right of the game screen
        text = font.render("Points: " + str(points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (900, 40)
        SCREEN.blit(text, textRect)

    def background():
        # creating the ground that the bunny will be running on
        global x_pos_bg, y_pos_bg
        image_width = BG[0].get_width()
        for i in range(0, 60):
            SCREEN.blit(BG[0], (image_width*i + x_pos_bg, y_pos_bg))
            for j in range(1, 14):
                SCREEN.blit(BG[1], (image_width*i + x_pos_bg, image_width*j + y_pos_bg))
        if x_pos_bg <= -image_width:
            x_pos_bg = 0
        x_pos_bg -= game_speed # moving the ground across the screen

    while run:
        for event in pygame.event.get():
            # exiting the game
            if event.type == pygame.QUIT:
                run = False
                sys.exit()
            # if the menu button is pressed, go to the main menu
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos  # gets mouse position
                if menuButtonObj.button.collidepoint(mouse_pos):
					# jump back to main menu
                    mainMenu.main()
        
        SCREEN.fill((135, 206, 235))
        userInput = pygame.mouse.get_pressed() # get whether or not the screen was touched
        fabric = False
        if GPIO.input(20): # check whether the conductive fabric was touched
            fabric = True
        player.draw(SCREEN)
        player.update(userInput, fabric)

        # if there are no more snakes, create a new one and add it to the list of snakes
        if len(snakes) == 0:
            snakes.append(Snake())
        
        for obstacle in snakes:
            obstacle.draw(SCREEN)
            obstacle.update()
            # if the bunny collides with the snake, the game ends
            if player.bunny_rect.colliderect(obstacle.rect):
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
            # rendering the UI for the very beginning 
            text = font.render("Press screen to Start", True, (0, 0, 0))
        else:
            # rendering the UI and displaying the score for when the player collides with a snake
            text = font.render("Press screen to Restart", True, (0, 0, 0))
            score = font.render("Your Score: " + str(points), True, (0, 0, 0))

            # positioning the score in the corner
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)
            SCREEN.blit(score, scoreRect)
        
        # displaying the instructions on the screen
        instruction = font.render("Touch the screen to jump over the snake", True, (0, 0, 0))
        instructionRect = instruction.get_rect()
        instructionRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
        SCREEN.blit(instruction, instructionRect)
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
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos 
                if menuButtonObj.button.collidepoint(mouse_pos):
                    # jump back to main menu
                    mainMenu.main()
                else:
                    main()
                
# menu(death_count=0)