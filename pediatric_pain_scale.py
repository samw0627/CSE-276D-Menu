import pygame
import os
import sys
from buttons import menuButton

import menu as mainMenu

# TODO: 
# Add in sounds if time


pygame.init()
clock = pygame.time.Clock()
fps = 60
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1024

FACE_HEIGHT = 150
FACE_WIDTH = 256

WAIT_TIME_SECONDS = 1

bg = [255, 244, 219]

BACKGROUND_IMG = 'carrots_assets/background.png'

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF)
# self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF )


class faceButton:
	"""
	Class for the pain scale buttons.
	Each button has an associated image and full screen image.
	"""
	def __init__(self, imgFileName, soundFileName, x, y) -> None:
		self.img = pygame.image.load(os.path.join("painscale_assets", imgFileName)).convert_alpha()
		self.img = pygame.transform.scale(self.img, (FACE_WIDTH, FACE_HEIGHT))
		self.sound = pygame.mixer.Sound(os.path.join("painscale_assets", soundFileName))
		self.fullscreenImg =  pygame.image.load(os.path.join("painscale_assets", imgFileName))
		self.fullscreenImgRect = self.fullscreenImg.get_rect()
		self.button = pygame.Rect(x, y, FACE_WIDTH, FACE_HEIGHT)


def showFullScreen(screen, faceButton, mouse_pos):
    # fill the screen with the background color to clear the original buttons
    # blit on the full screen image, and update the display
    # wait specified time, then go back to the original display
    print('button was pressed at {0}'.format(mouse_pos))
    pygame.mixer.Sound.play(faceButton.sound)
    pygame.time.wait(int(0.05 * 1000))
    screen.fill(bg)
    # self._display_surf.blit(self.display_face, TOP_LEFT)
    screen.blit(faceButton.fullscreenImg, faceButton.fullscreenImgRect)
    pygame.display.update()
    pygame.time.wait(int(WAIT_TIME_SECONDS * 1000))
    screen.fill(bg)


def main(): 
	# create all facebutton objects
	faceXStartCoords = 50
	faceYUpperRowCoords = 125
	faceYLowerRowCoords = 375

	faceWidthOffsets = FACE_WIDTH + 75

	rank0Face = faceButton("Rank0Face.png", "cat_rank0_meow.wav", faceXStartCoords, faceYUpperRowCoords)
	rank1Face = faceButton("Rank1Face.png", "cat_rank1_meow.wav", faceXStartCoords + faceWidthOffsets * 1, faceYUpperRowCoords)
	rank2Face = faceButton("Rank2Face.png", "cat_rank2_meow.wav", faceXStartCoords + faceWidthOffsets * 2, faceYUpperRowCoords)
	rank3Face = faceButton("Rank3Face.png", "cat_rank3_meow.wav", faceXStartCoords + faceWidthOffsets * 0, faceYLowerRowCoords)
	rank4Face = faceButton("Rank4Face.png", "cat_rank4_meow.wav", faceXStartCoords + faceWidthOffsets * 1, faceYLowerRowCoords)
	rank5Face = faceButton("Rank5Face.png", "cat_rank5_meow.wav", faceXStartCoords + faceWidthOffsets * 2, faceYLowerRowCoords)

	# create menu button object
	menuButtonObj = menuButton("test_hamburg_menu.png")

	screen.fill(bg)
	# background = pygame.image.load(BACKGROUND_IMG) 
	# screen.blit(background, (0, 0))

	# main game loop
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				# pygame.display.quit()
				sys.exit()

			if event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = event.pos  # gets mouse position

				if rank0Face.button.collidepoint(mouse_pos):
					showFullScreen(screen, rank0Face, mouse_pos)
				elif rank1Face.button.collidepoint(mouse_pos):
					showFullScreen(screen, rank1Face, mouse_pos)
				elif rank2Face.button.collidepoint(mouse_pos):
					showFullScreen(screen, rank2Face, mouse_pos)
				elif rank3Face.button.collidepoint(mouse_pos):
					showFullScreen(screen, rank3Face, mouse_pos)
				elif rank4Face.button.collidepoint(mouse_pos):
					showFullScreen(screen, rank4Face, mouse_pos)
				elif rank5Face.button.collidepoint(mouse_pos):
					showFullScreen(screen, rank5Face, mouse_pos)
				elif menuButtonObj.button.collidepoint(mouse_pos):
					# jump back to main menu
					mainMenu.main()

		# draw all buttons
		# bg = background color, otherwise the blitted image will have a background color
		pygame.draw.rect(screen, bg, rank0Face.button) 
		pygame.draw.rect(screen, bg, rank1Face.button) 
		pygame.draw.rect(screen, bg, rank2Face.button)
		pygame.draw.rect(screen, bg, rank3Face.button)
		pygame.draw.rect(screen, bg, rank4Face.button)
		pygame.draw.rect(screen, bg, rank5Face.button)

		# draw menu button
		pygame.draw.rect(screen, bg, menuButtonObj.button)

		# blit on all buttons
		screen.blit(rank0Face.img, rank0Face.img.get_rect(center = rank0Face.button.center))
		screen.blit(rank1Face.img, rank1Face.img.get_rect(center = rank1Face.button.center))
		screen.blit(rank2Face.img, rank2Face.img.get_rect(center = rank2Face.button.center))
		screen.blit(rank3Face.img, rank3Face.img.get_rect(center = rank3Face.button.center))
		screen.blit(rank4Face.img, rank4Face.img.get_rect(center = rank4Face.button.center))
		screen.blit(rank5Face.img, rank5Face.img.get_rect(center = rank5Face.button.center))

		# blit on menu button image
		screen.blit(menuButtonObj.img, menuButtonObj.img.get_rect(center = menuButtonObj.button.center))
		
		pygame.display.update()
		clock.tick(fps)