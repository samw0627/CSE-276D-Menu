import pygame
import pygame_menu

pygame.init()
surface = pygame.display.set_mode((600, 400))


def start_pain_scale():
    # Do the job here !
    pass

def start_bunny_game():
    # Do the job here !
    pass

def start_bunny_face():
    # Do the job here !
    pass

menu = pygame_menu.Menu('BunnyBot', 600, 400,
                       theme=pygame_menu.themes.THEME_SOLARIZED)
HELP = 'Hello there! Select a mode to begin. ' \

menu.add.label(HELP, max_char=-1, font_size=20)
menu.add.button('Pain Scale', start_pain_scale)
menu.add.button('Bunny Game', start_bunny_game)
menu.add.button('Bunny Face', start_bunny_face)

menu.add.button('Quit', pygame_menu.events.EXIT)

menu.mainloop(surface)
