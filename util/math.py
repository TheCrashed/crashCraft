from __future__ import absolute_import

import math


def cosd(degrees):
	return math.degrees(math.cos(math.radians(degrees)))

def sind(degrees):
	return math.degrees(math.sin(math.radians(degrees)))

def degree_to_byte(degree):
	while degree >= 360:
		degree -= 360
	while degree < 0:
		degree += 360

	return int((degree * 256.0 / 360.0))
