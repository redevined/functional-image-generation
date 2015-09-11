#!/usr/bin/env python

from __future__ import division
import random, math
import time
from figen import fixImage, varImage


def toRGB(hue, sat = 1, val = 1) :
	r = (1 - abs((hue / 60) % 2 - 1)) if 60 <= hue < 120 or 240 <= hue < 300 else int(hue not in range(120, 240))
	g = (1 - abs((hue / 60) % 2 - 1)) if 0 <= hue < 60 or 180 <= hue < 240 else int(hue not in range(240, 360))
	b = (1 - abs((hue / 60) % 2 - 1)) if 120 <= hue < 180 or 300 <= hue < 360 else int(hue not in range(0, 120))
	return [ int((c * sat + 1 - sat) * val * 255) for c in (r, g, b) ]


width = 4096
height = 4096

@fixImage(width, height)
def julia(x, y) :
	resolution = 4096
	zoom = 0.7

	def iterate(limit, zoom) :
		zx = (x - (width / 2)) / (width / 2 * zoom)
		zy = (y - (height / 2)) / (height / 2 * zoom)

		z = zx + zy * 1j
		c = 0.39 + 0.35j

		for it in range(limit) :
			if z.real**2 + z.imag**2 < 4 :
				z = z**2 + c
			else :
				return it
		return limit

	val = iterate(resolution, zoom)
	#return toRGB(int( (val % 256) / 256 * 360 ), 0.8, int(val < resolution)) # rainbow!
	return [ int(255 * (abs(50 - val) / 50)**i) % 256 for i in (3, .7, .5) ]


def main() :
	#julia.generate().show()
	julia.render("test-{0}.png".format(int(time.time())))


if __name__ == "__main__" :
	main()
