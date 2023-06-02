import pygame
import os
import sys


"""
I decided to put the general menu button in its own file.
It's basically the same as the face buttons in the pain scale,
but with less things.
"""

class menuButton:
	"""
	The button is just a rectangle, so any rect() methods in pygame should work for it
	"img" is the image that will appear on the button. Ideally we leave all menu assets
	in the menu_assets folder, and upon creation specify which file to use for this button.
	
    """
	def __init__(self, imgFileName, xCoords=100, yCoords=100, width=50, height=50) -> None:
		self.width = width
		self.height = height
		self.img = pygame.image.load(os.path.join("menu_assets", imgFileName)).convert_alpha()
		self.img = pygame.transform.scale(self.img, (self.width, self.height))
		self.button = pygame.Rect(xCoords, yCoords, self.width, self.height)


