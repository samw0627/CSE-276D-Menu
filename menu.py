#import necessary packages
import pygame
import pygame_menu
import bunnyjump
import pediatric_pain_scale
from faces_game import control
import  carrots_game 
from utils import *

#Initailize pygame
pygame.init()
#Set the screen size
surface = pygame.display.set_mode((WIDTH, HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.FULLSCREEN)

#Function to start the pain scale
def start_pain_scale():
    pediatric_pain_scale.main()

#Function to start bunny scrolling game
def start_bunny_game():
    bunnyjump.menu(death_count=0)

#Function to start bunny face game
def start_bunny_face():
    # Do the job here !
    control_ = control()
    control_.on_execute()

#Function to start carrots game
def start_carrots_game():
    carrots_game.show_menu(NUM_HEARTS, 0)

#Function to start the menu
def main():
    #Setting the theme of the menu
    menu = pygame_menu.Menu('BunnyBot', WIDTH, HEIGHT,
                        theme=pygame_menu.themes.THEME_SOLARIZED)
    HELP = 'Hello there! Select a mode to begin. ' \
    #Place buttons on menu
    menu.add.label(HELP, max_char=-1, font_size=20)
    menu.add.button('Pain Scale', start_pain_scale)
    menu.add.button('Bunny Game', start_bunny_game)
    menu.add.button('Bunny Face', start_bunny_face)
    menu.add.button('Carrots Game', start_carrots_game)

    #Quit button
    menu.add.button('Quit', pygame_menu.events.EXIT)
    #Loop such that the menu is always displayed
    menu.mainloop(surface)

#Run the main function from other features
if __name__ == "__main__":
    main()
