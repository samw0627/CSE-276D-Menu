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
	DEFAULT_X = 20
	DEFAULT_Y = 20
	DEFAULT_WIDTH = 75
	DEFAULT_HEIGHT = 75

	def __init__(self, imgFileName, x=DEFAULT_X, y=DEFAULT_Y, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT) -> None:
		self.width = width
		self.height = height
		self.x = x
		self.y = y
		self.img = pygame.image.load(os.path.join("menu_assets", imgFileName)).convert_alpha()
		self.img = pygame.transform.scale(self.img, (self.width, self.height))
		self.button = pygame.Rect(self.x, self.y, self.width, self.height)
	
	def moveButton(self, x, y):
		"""
		Move the button to a new x,y location.
		"""
		self.x = x
		self.y = y
		self.button = pygame.Rect(self.x, self.y, self.width, self.height)

	def resizeButton(self, width, height):
		"""
		Resize the button to a new width, height.
		The button image is also be resized to fit on top of the button rect.
		"""
		self.width = width
		self.height = height
		self.button = pygame.Rect(self.x, self.y, self.width, self.height)
		self.img = pygame.transform.scale(self.img, (self.width, self.height))
	
	def changeImg(self, imgFileName):
		"""
		Change the image placed on top of the button.
		"""
		self.img = pygame.image.load(os.path.join("menu_assets", imgFileName)).convert_alpha()
		self.img = pygame.transform.scale(self.img, (self.width, self.height))