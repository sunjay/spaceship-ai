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
	ship.position = [WIDTH / 4, HEIGHT / 2 - 30]
	ship.rotation = -90
	scene.add_object(ship)

	ship2 = Spaceship(scene, color=(255, 10, 10))
	ship2.position = [WIDTH - WIDTH / 4, HEIGHT / 2 - 30]
	ship2.rotation = 90
	scene.add_object(ship2)

	BARRIERS_X = 10
	BARRIERS_Y = 10
	for i in xrange(BARRIERS_Y):
		y = int(HEIGHT / BARRIERS_Y * (i + 0.5))
		left_offset = ((i % 2) == 0) * 50
		for j in xrange(BARRIERS_X):
			barrier = Circle(scene, 5)

			x = int(WIDTH / BARRIERS_X * (j + 0.5) + left_offset)
			barrier.position = [x, y]
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
