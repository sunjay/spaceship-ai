"""
Spaceship Artificial Intelligence
"""
from math import sin, cos, radians, atan2, hypot, pi

import pygame

from const import (WIDTH, HEIGHT, BOTTOM_BOUNDARY, LEFT_BOUNDARY,
	RIGHT_BOUNDARY, TOP_BOUNDARY, BOUNDARIES)

__author__ = 'Sunjay'

# Since the angle is calculated as a floating point number,
# this threshold dictates what valid range is acceptable
# radians(1) says that within 1 degree is okay
RAY_ANGLE_THRESHOLD = radians(1)  # radians
# Objects at a distance less than or equal to this will
# be avoided.
AVOIDANCE_DISTANCE = 150
# The maximum angle to be used to avoid an object
AVOIDANCE_ANGLE = 30  # degrees
# The maximum angle that the ship can turn in any given frame
MAX_TURN_ANGLE = 1  # degrees

# Debug ray tracing
DEBUG_RAY = False


class Spaceship(object):

	def __init__(self, scene, width=20, height=30, color=(0, 128, 255)):
		self.scene = scene
		self.color = color
		self.width = width
		self.height = height

		self.rotation = 0  # degrees counterclockwise from north
		self.position = [0, 0]
		self.speed = 3

		self._desired_angle = None

	def get_screen_width(self):
		return WIDTH

	def get_screen_height(self):
		return HEIGHT

	def render(self, screen):
		ship_surface = pygame.Surface((self.width, self.height))
		ship_surface.set_colorkey((0, 0, 0))

		# These points could probably be described better...
		pts = [
			(0, int(self.height * 0.8)),
			(self.width, int(self.height * 0.8)),
			(self.width / 2, 0),
		]
		pygame.draw.polygon(ship_surface, self.color, pts)

		body_rect = pygame.Rect(int(self.width * 0.2), 0, int(self.width * 0.6), self.height)
		pygame.draw.ellipse(ship_surface, self.color, body_rect)

		if self.rotation % 360 != 0:
			ship_surface = pygame.transform.rotate(ship_surface, self.rotation)

		pos = list(self.position)
		pos[0] -= ship_surface.get_width() / 2
		pos[1] -= ship_surface.get_height() / 2
		screen.blit(ship_surface, pos)

		if DEBUG_RAY:
			ray_angle = radians(self.rotation)
			ray_x = AVOIDANCE_DISTANCE * sin(ray_angle)
			ray_y = AVOIDANCE_DISTANCE * cos(ray_angle)

			x, y = self.position
			pygame.draw.line(screen, (255, 0, 0), (x, y), (x - ray_x, y - ray_y), 3)

	def get_scene_objects(self):
		return self.scene.get_objects()

	def distance_to(self, obj):
		"""
		Return the distance to the given object
		"""
		x, y = self.position
		obj_x, obj_y = obj.position
		return hypot(x - obj_x, y - obj_y)

	def distance_to_boundary(self, boundary):
		"""
		Boundary constants:
			LEFT_BOUNDARY, RIGHT_BOUNDARY,
			TOP_BOUNDARY, BOTTOM_BOUNDARY
		"""
		if boundary == LEFT_BOUNDARY:
			return self.position[0]
		elif boundary == RIGHT_BOUNDARY:
			return self.get_screen_width() - self.position[0]
		elif boundary == TOP_BOUNDARY:
			return self.position[1]
		elif boundary == BOTTOM_BOUNDARY:
			return self.get_screen_height() - self.position[1]
		else:
			raise ValueError("Invalid boundary")

	def ray_cast(self, max_distance):
		"""
		Casts a ray forward and detects the first object or boundary
		found in the ray's path

		Returns an object if it is found or a boundary constant if a boundary
		is found
		Boundary constants:
			LEFT_BOUNDARY, RIGHT_BOUNDARY,
			TOP_BOUNDARY, BOTTOM_BOUNDARY
		Returns None if nothing is found
		"""
		ray_angle = radians(self.rotation)

		# Sense objects
		x, y = self.position
		closest = None
		closest_distance = float('inf')
		for obj in self.get_scene_objects():
			if not hasattr(obj, 'position') or obj is self:
				continue
			obj_x, obj_y = obj.position

			# Figure out what the angle of this object is
			# relative to self
			delta_x = obj_x - x
			delta_y = y - obj_y
			angle = atan2(delta_y, delta_x) - pi/2

			# If the angle is acceptably in front of self
			if abs(angle - ray_angle) >= RAY_ANGLE_THRESHOLD:
				continue

			dist = self.distance_to(obj)
			if dist < closest_distance:
				closest = obj
				closest_distance = dist

		if closest is not None:
			if closest_distance <= max_distance:
				return closest
			# Object is there, but not close enough
			return None

		# Sense boundary

		# Divide the max_distance into components
		# based on the ray angle
		max_x = max_distance * sin(ray_angle)
		max_y = max_distance * cos(ray_angle)

		# Add the max_x and max_y to the current position
		max_x = x - max_x
		max_y = y - max_y

		# Check if either component is out of a boundary
		if max_x < 0:
			return LEFT_BOUNDARY
		elif max_x > self.get_screen_width():
			return RIGHT_BOUNDARY
		elif max_y < 0:
			return TOP_BOUNDARY
		elif max_y > self.get_screen_height():
			return BOTTOM_BOUNDARY

		# Nothing found
		return None

	def update(self):
		# Sense boundaries

		# Sense objects
		found = self.ray_cast(AVOIDANCE_DISTANCE)
		if found is not None:
			# Object is ahead, avoid it!

			# Figure out how much distance is left between
			# this object and the object in question
			if found in BOUNDARIES:
				dist = self.distance_to_boundary(found)
			else:
				dist = self.distance_to(found)

			dist_left = AVOIDANCE_DISTANCE - dist

			# Rotate by this much to avoid
			angle = self.rotation + AVOIDANCE_ANGLE
			self._desired_angle = angle

		# Tween smoothly to the desired angle if any
		if self._desired_angle is not None:
			# The sign (positive or negative) of the turn to take based on the
			# current and desired rotation angle
			angle_delta = self._desired_angle - self.rotation
			# If the desired angle has been reached
			if abs(angle_delta) < MAX_TURN_ANGLE:
				self._desired_angle = None
			else:
				# Normalize
				turn_sign = angle_delta / abs(angle_delta)
				turn_angle = MAX_TURN_ANGLE * turn_sign
				self.rotation += turn_angle

		# Update position
		rotation_angle = radians(self.rotation)
		self.position[0] -= int(self.speed * sin(rotation_angle))
		self.position[1] -= int(self.speed * cos(rotation_angle))
