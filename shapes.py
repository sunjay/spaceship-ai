import pygame

__author__ = 'Sunjay'


class Circle(object):

	def __init__(self, scene, radius=20, color=(0, 0, 0)):
		self.scene = scene
		self.radius = radius
		self.color = color

		self.position = [0, 0]

	@property
	def width(self):
		return self.radius * 2

	@property
	def height(self):
		return self.radius * 2

	def update(self):
		pass

	def render(self, screen):
		pygame.draw.circle(screen, self.color, self.position, self.radius)
