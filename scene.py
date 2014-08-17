import pygame


class Scene(object):
	def __init__(self, background=(0, 0, 0)):
		self.background = background

		self.__objects = []

	def add_object(self, obj):
		self.__objects.append(obj)

	def remove_object(self, obj):
		self.__objects.remove(obj)

	def has_object(self, obj):
		return obj in self.__objects

	def get_objects(self):
		for obj in self.__objects:
			yield obj

	def update(self):
		# Update objects
		for obj in self.get_objects():
			obj.update()

	def render(self, screen):
		# Clear screen
		screen.fill(self.background)

		# Render everything
		for obj in self.get_objects():
			obj.render(screen)

		# Flip the buffer
		pygame.display.flip()
