#!/usr/bin/env python

"""
FIGen - Functional Image Generation Library

Some test functions.

"""

from __future__ import division
import os, random

from figen import fixImage, varImage, colors
from tools import instant, Struct, Timer


img = Struct(
	width = 2560,
	height = 1440,
	limit = 512,
	zoom = 0.9,
	c = -0.8 - 0.156j
)


@fixImage(img.width, img.height)
def julia(x, y, rgb) :
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
	return rgb(val)


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


def showOne() :
	julia(lambda val : colors.ice(val, 150)).show()


def saveAll() :
	rgb_funcs = (
		lambda val : colors.ice(val, 150),
		lambda val : colors.grayscale(val, 150),
		lambda val : colors.rainbow(val, img.limit),
		lambda val : colors.helpers.invert(*colors.ice(val, 150)),
		lambda val : colors.helpers.invert(*colors.grayscale(val, 150)),
		lambda val : colors.helpers.invert(*colors.rainbow(val, img.limit))
	)
	for func in rgb_funcs :
		filedir = "images"
		filename = "julia_{width}x{height}_{zoom}_{c}_{id}".format(id = hex(id(func))[2:], **img).replace(".", "") + ".png"
		julia(func).save(os.path.join(filedir, filename))


@instant
@Timer
def main() :
	saveAll()
