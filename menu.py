import pygame
import pygame_menu
import bunnyjump
import pediatric_pain_scale
from faces_game import control
import  carrots_game 
from utils import *

pygame.init()
surface = pygame.display.set_mode((WIDTH, HEIGHT))

def start_pain_scale():
    # Do the job here !
    pediatric_pain_scale.main()
    # pass

def start_bunny_game():
    # Do the job here !
    bunnyjump.menu(death_count=0)
    # pass

def start_bunny_face():
    # Do the job here !
    control_ = control()
    control_.on_execute()
    
def start_carrots_game():
    carrots_game.show_menu(NUM_HEARTS, 0)

def main():
    menu = pygame_menu.Menu('BunnyBot', WIDTH, HEIGHT,
                        theme=pygame_menu.themes.THEME_SOLARIZED)
    HELP = 'Hello there! Select a mode to begin. ' \

    menu.add.label(HELP, max_char=-1, font_size=20)
    menu.add.button('Pain Scale', start_pain_scale)
    menu.add.button('Bunny Game', start_bunny_game)
    menu.add.button('Bunny Face', start_bunny_face)
    menu.add.button('Carrots Game', start_carrots_game)

    menu.add.button('Quit', pygame_menu.events.EXIT)

    menu.mainloop(surface)

if __name__ == "__main__":
    main()
