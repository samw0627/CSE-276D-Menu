import pygame
import os
import sys
from buttons import menuButton

import menu

# make menu button

pygame.init()
clock = pygame.time.Clock()
fps = 60
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1024

FACE_HEIGHT = 100
FACE_WIDTH = 125

WAIT_TIME_SECONDS = 1

bg = [255, 255, 255]

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class faceButton:
	def __init__(self, imgFileName, x, y) -> None:
		self.img = pygame.image.load(os.path.join("painscale_assets", imgFileName)).convert_alpha()
		self.img = pygame.transform.scale(self.img, (FACE_WIDTH, FACE_HEIGHT))
		self.fullscreenImg = pygame.transform.scale(self.img, (SCREEN_WIDTH, SCREEN_HEIGHT))
		self.fullscreenImgRect = self.fullscreenImg.get_rect()
		self.button = pygame.Rect(x, y, FACE_WIDTH, FACE_HEIGHT)


def showFullScreen(screen, faceButton, mouse_pos):
    # fill the screen with the background color to clear the original buttons
    # blit on the full screen image, and update the display
    # wait specified time, then go back to the original display
    print('button was pressed at {0}'.format(mouse_pos))
    pygame.time.wait(int(0.05 * 1000))
    screen.fill(bg)
    screen.blit(faceButton.fullscreenImg, faceButton.fullscreenImgRect)
    pygame.display.update()
    pygame.time.wait(int(WAIT_TIME_SECONDS * 1000))
    screen.fill(bg)


def main(): 
	# create all facebutton objects
	faceXStartCoords = 35
	faceYCoords = 200
	faceWidthOffsets = 165

	rank0Face = faceButton("smile_1.png", faceXStartCoords, faceYCoords)
	rank1Face = faceButton("smile_1.png", faceXStartCoords + faceWidthOffsets * 1, faceYCoords)
	rank2Face = faceButton("smile_1.png", faceXStartCoords + faceWidthOffsets * 2, faceYCoords)
	rank3Face = faceButton("smile_1.png", faceXStartCoords + faceWidthOffsets * 3, faceYCoords)
	rank4Face = faceButton("smile_1.png", faceXStartCoords + faceWidthOffsets * 4, faceYCoords)
	rank5Face = faceButton("smile_1.png", faceXStartCoords + faceWidthOffsets * 5, faceYCoords)

	# create menu button object
	menuButtonObj = menuButton("test_hamburg_menu.png")

	screen.fill(bg)

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
					menu.main()

		# draw all buttons
		# bg = background color, otherwise the blitted image will have a background color
		# that is the screen bg color
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
		screen.blit(rank2Face.img, rank2Face.img.get_rect(center = rank3Face.button.center))
		screen.blit(rank2Face.img, rank2Face.img.get_rect(center = rank4Face.button.center))
		screen.blit(rank2Face.img, rank2Face.img.get_rect(center = rank5Face.button.center))

		# blit on menu button image
		screen.blit(menuButtonObj.img, menuButtonObj.img.get_rect(center = menuButtonObj.button.center))
		
		pygame.display.update()
		clock.tick(fps)