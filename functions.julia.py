#!/usr/bin/env python

from __future__ import division
from figen import fixImage, varImage, colors
from tools import Struct, Timer


img = Struct(
	width = 2560,
	height = 1440,
	limit = 512,
	zoom = 0.9,
	c = -0.8 - 0.156j
)


@fixImage(img.width, img.height)
def julia(x, y) :
	ratio = img.width / img.height

	def iterate() :
		zx = (x - (img.width / 2)) / (img.width / 2 * img.zoom) * ratio
		zy = (y - (img.height / 2)) / (img.height / 2 * img.zoom)

		z = zx + zy * 1j
		c = img.c

		for it in range(img.limit) :
			if z.real**2 + z.imag**2 <= 4 :
				z = z**2 + c
			else :
				return it
		return img.limit

	val = iterate()
	return colors.ice(val, 150)