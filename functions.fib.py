#!/usr/bin/env python

from __future__ import division
from figen import fixImage, varImage, colors
from tools import Struct, Timer


img = Struct(
	width = 256,
	height = 256
)


@fixImage(img.width, img.height)
def fib(x, y) :
	a = b = 1
	for _ in range(x - 1) :
		a, b = b, a + b
	return (b % 255,) * 3
