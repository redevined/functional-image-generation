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
		sat = 0.8
		_val = int(val < limit)
		r, g, b = self.helpers.convertHSV(hue, sat, _val)
		return r, g, b


	def ice(self, val, limit) :
		c = abs(limit - val) / limit
		r, g, b = (int(255 * c**p) % 256 for p in (3, .7, .5))
		return r, g, b

	@singleton
	class helpers(object) :

		def convertHSV(self, hue, sat = 1, val = 1) :
			r = (1 - abs((hue // 60) % 2 - 1)) if 60 <= hue < 120 or 240 <= hue < 300 else int(not (120 <= hue < 240))
			g = (1 - abs((hue // 60) % 2 - 1)) if 0 <= hue < 60 or 180 <= hue < 240 else int(not (240 <= hue < 360))
			b = (1 - abs((hue // 60) % 2 - 1)) if 120 <= hue < 180 or 300 <= hue < 360 else int(not (0 <= hue < 120))
			return [ int((c * sat + 1 - sat) * val * 255) for c in (r, g, b) ]
