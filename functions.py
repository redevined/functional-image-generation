#!/usr/bin/env python

"""
FIGen - Functional Image Generation Library

Some test functions.

"""

from __future__ import division
import os, random

from figen import fixImage, varImage, colors
from tools import instant, Struct, Timer


def convertHSV(hue, sat = 1, val = 1) :
	r = (1 - abs((hue / 60) % 2 - 1)) if 60 <= hue < 120 or 240 <= hue < 300 else int(hue not in range(120, 240))
	g = (1 - abs((hue / 60) % 2 - 1)) if 0 <= hue < 60 or 180 <= hue < 240 else int(hue not in range(240, 360))
	b = (1 - abs((hue / 60) % 2 - 1)) if 120 <= hue < 180 or 300 <= hue < 360 else int(hue not in range(0, 120))
	return [ int((c * sat + 1 - sat) * val * 255) for c in (r, g, b) ]


def grayscale(val) :
	return [ int(255 * (abs(50 - val) / 50)) ] * 3


def rainbow(val) :
	return convertHSV(int( (val % 256) / 256 * 360 ), 0.8, int(val < jconf.limit))


def ice(val) :
	return [ int(255 * (abs(50 - val) / 50)**i) % 256 for i in (3, .7, .5) ]


jconf = Struct(
	width = 2560,
	height = 1440,
	limit = 512,
	zoom = 0.7,
	color_func = ice,
	c = -0.595 - 0.45j
)


@fixImage(jconf.width, jconf.height)
def julia(x, y) :
	ratio = jconf.width / jconf.height

	def iterate() :
		zx = (x - (jconf.width / 2)) / (jconf.width / 2 * jconf.zoom) * ratio
		zy = (y - (jconf.height / 2)) / (jconf.height / 2 * jconf.zoom)

		z = zx + zy * 1j
		c = jconf.c

		for it in range(jconf.limit) :
			if z.real**2 + z.imag**2 <= 4 :
				z = z**2 + c
			else :
				return it
		return jconf.limit

	val = iterate()
	return jconf.color_func(val)


@instant
@Timer
def main() :
	for f in (ice, grayscale, rainbow) :
		jconf.color_func = f
		filedir = "images"
		filename = "julia_{width}x{height}_{zoom}_{limit}_{c}_{color_func.__name__}".format(**jconf).replace(".", "") + ".png"
		julia().save(os.path.join(filedir, filename))
