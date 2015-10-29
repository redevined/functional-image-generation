#!/usr/bin/env python

from __future__ import division
from random import randint
from figen import fixImage, varImage, colors
from tools import Struct, Timer


img = Struct(
	width = 512,
	height = 512,
	n = 40
)
img.points = {
	(randint(1, img.width), randint(1, img.height)) : color
	for color in (
		colors.helpers.convertHSV(randint(60, 300), 0.8)
		for _ in range(img.n)
	)
}

@fixImage(img.width, img.height)
def voronoi(x, y) :
	d = nearest = None
	dist = lambda a, b : ((a[0] - b[0])**2 + (a[1] - b[1])**2)**0.5

	for point in img.points.keys() :
		dn = dist(point, (x, y))
		if d is None or d > dn :
			d = dn
			nearest = point

	color = img.points[nearest]
	return color