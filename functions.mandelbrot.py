#!/usr/bin/env python

from __future__ import division
from figen import fixImage, varImage, colors
from tools import Struct, Timer


@fixImage(1024, 1024)
def mandelbrot(x, y) :
	limit = 880
	zoom = 8e-9
	dx = 0.356888
	dy = 0.645411
	colors = [3, 0.5, 0.7]

	def iterate() :
		z = complex(0)
		for n in range(1, limit) :
			if z.real**2 + z.imag**2 < 4 :
				add = (
					(x * zoom + dx) +
					(y * zoom - dy) * 1j
				)
				z = z**2 + add
			else :
				return n
		return limit

	val = iterate()
	return [
		int(abs((val - 80) / 800.0)**color * 255)
		for color in colors
	]
