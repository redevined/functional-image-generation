#!/usr/bin/env python

"""
FIGen - Functional Image Generation Library

This library allows the simple creation of images through a provided function.
Just decorate your function with one of the decorators.

Functions:
	fixImage:
		Decorate a function with a width and height fixed at function declaration.
	varImage:
		Pass width and height to the function on invocation.

"""

from __future__ import division
import numpy
from PIL import Image

from tools import decorator, singleton


def fixImage(width, height) :
	@decorator
	def generate(func, *args, **kwargs) :
		rows = list()
		for y in range(height) :
			row = list()
			for x in range(width) :
				try :
					r, g, b = func(x, y, *args, **kwargs)
					row.append((r, g, b))
				except TypeError :
					raise TypeError("function takes at least 0 arguments")
				except ValueError :
					raise ValueError("rendering function did not return a 3-tupel of RGB values")
				except Exception as e :
					raise e.__class__("unknown error occured during function execution: " + e.message)
			rows.append(row)
		return Image.fromarray(numpy.array(rows, dtype = "uint8"))
	generate.__name__ = fixImage.__name__
	return generate


@decorator
def varImage(func, width, height, *args, **kwargs) :
	rows = list()
	for y in range(height) :
		row = list()
		for x in range(width) :
			try :
				r, g, b = func(x, y, width, height, *args, **kwargs)
				row.append((r, g, b))
			except TypeError :
				raise TypeError("function takes at least 2 arguments")
			except ValueError :
				raise ValueError("rendering function did not return a 3-tupel of RGB values")
			except Exception as e :
				raise e.__class__("unknown error occured during function execution: " + e.message)
		rows.append(row)
	return Image.fromarray(numpy.array(rows, dtype = "uint8"))


@singleton
class colors(object) :

	def grayscale(self, val, limit) :
		c = abs(limit - val) / limit
		r = g = b = int(255 * c)
		return r, g, b

	def rainbow(self, val, limit) :
		hue = (val % 256) / 256 * 360
		r, g, b = self.helpers.convertHSV(hue)
		return r, g, b

	def ice(self, val, limit) :
		c = abs(limit - val) / limit
		r, g, b = (int(255 * c**p) % 256 for p in (3, .7, .5))
		return r, g, b

	@singleton
	class helpers(object) :

		def invert(self, r, g, b) :
			return [ 255 - c for c in (r, g, b) ]

		def convertHSV(self, hue, sat = 1, val = 1) :
			c = 1 - abs((hue / 60) % 2 - 1)
			r, g, b = [
				(1, c, 0),
				(c, 1, 0),
				(0, 1, c),
				(0, c, 1),
				(c, 0, 1),
				(1, 0, c)
			][int(hue // 60 % 6)]
			return [ int((color * sat + 1 - sat) * val * 255) for color in (r, g, b) ]
