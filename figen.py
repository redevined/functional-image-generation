#!/usr/bin/env python

"""
FIGen - Functional Image Generation Library

This library allows the simple creation of images through a provided function.
Just decorate your function with an ImageGenerator object and call render on the function to create an image.

Classes:
	ImageGenerator:
		Instances of this class can render images from an input function. Can be used as an decorator.

Usage:
	@ImageGenerator(600, 400)
	def example(x, y) :
		val = int(((x + y) / 1000.0) * 255)
		return val, val, val

	example.render("example.png")

	# OR

	def example2(x, y) :
		val = int((1 - ((x + y) / 1000.0)) * 255)
		return val, val, val

	image = ImageGenerator(600, 400)
	image.register(example2)
	image.generate().show()

	# OR

	ImageGenerator(600, 400)(lambda x, y : [int(((x + y) / 1000.0) * 255)] * 3).render("example.png")

"""

import numpy
from PIL import Image


class ImageGenerator(object) :
	"""
	ImageGenerator Class

	Allows simple image generation through a function.
	The provided function will be called with the pixel coordinates for each pixel in the later image, starting from 0.

	Attributes:
		width -> int:
			Width of the resulting image.
		height -> int:
			Height of the resulting image.

	Methods:
		__init__(width, height):
			Constructor, takes width and height for image.
		__call__(func) -> self:
			Implicit caller, enables usage of class as decorator.
		register(func):
			Sets internal algorithm for image creation.
		render(filename = None, format = None):
			Generates image and saves it as a file if filename is provided.
		generate() -> PIL.Image.Image:
			Creates image by calling internal algorithm for each pixel.
		save(filename, format = None):
			Saves internal image as a file with specified format, if provided.
		show():
			Opens internal image in default image viewer.

	"""

	def __init__(self, width, height) :
		self.width = width
		self.height = height
		self._img = None
		self._algorithm = lambda x, y : (0, 0, 0)

	def __call__(self, func) :
		self.register(func)
		return self

	def register(self, func) :
		self._algorithm = func

	def render(self, filename = None, format = None) :
		self._img = self.generate()
		if filename :
			self.save(filename, format)

	def generate(self) :
		rows = list()
		for y in range(self.height) :
			row = list()
			for x in range(self.width) :
				try :
					r, g, b = self._algorithm(x, y)
					row.append((r, g, b))
				except ValueError :
					raise ValueError("Rendering algorithm did not return a 3-tupel of RGB values")
			rows.append(row)
		return Image.fromarray(numpy.array(rows, dtype = "uint8"))

	def save(self, filename, format = None) :
		try :
			self._img.save(filename, format)
		except AttributeError :
			raise AttributeError("Image has not been rendered yet")

	def show(self) :
		try :
			self._img.show()
		except AttributeError :
			raise AttributeError("Image has not been rendered yet")
