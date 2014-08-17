"""
The mainloop
"""
import pygame

from const import WIDTH, HEIGHT, BACKGROUND
from scene import Scene
from shapes import Circle
from spaceship import Spaceship

__author__ = 'Sunjay'


def quit_game():
	pygame.quit()


def main():
	pygame.init()
	pygame.display.set_caption("Spaceship AI Test")
	screen = pygame.display.set_mode((WIDTH, HEIGHT))

	scene = Scene(BACKGROUND)

	ship = Spaceship(scene)
	ship.position = [WIDTH / 2, HEIGHT / 2]
	scene.add_object(ship)

	barrier = Circle(scene, 20)
	barrier.position = [WIDTH / 2, HEIGHT / 8]
	scene.add_object(barrier)

	clock = pygame.time.Clock()

	while True:
		# Handle events
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return quit_game()

		pressed = pygame.key.get_pressed()
		if pressed[pygame.K_F4] and (pressed[pygame.K_LALT] or pressed[pygame.K_RALT]):
			return quit_game()

		scene.update()
		scene.render(screen)

		clock.tick(60)

if __name__ == "__main__":
	main()