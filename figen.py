#!/usr/bin/env python

"""
FIGen - Functional Image Generation Library

This library allows the simple creation of images through a provided function.
Just decorate your function with an ImageGenerator.

Functions:
	fixImage:
		Decorate a function with a width and height fixed at function declaration.
	varImage:
		Pass width and height to the function on invocation.

"""

import numpy
from PIL import Image


def fixImage(width, height) :
	def decorator(func) :
		def generate(*args, **kwargs) :
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
		generate.__name__ = func.__name__
		return generate
	return decorator

def varImage(func) :
	def generate(width, height, *args, **kwargs) :
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
	generate.__name__ = func.__name__
	return generate
