#!/usr/bin/env python

"""
FIGen - Functional Image Generation Library

Tools for FIGen.

"""

import time


def decorator(dec) :
	def outer(func) :
		def inner(*args, **kwargs) :
			return dec(func, *args, **kwargs)
		inner.__name__ = func.__name__
		return inner
	outer.__name__ = dec.__name__
	return outer


def singleton(cls) :
	return cls()


def recurse(func) :
	return lambda *args, **kwargs : func(func, *args, **kwargs)


class Struct(dict) :

	def __init__(self, obj = {}, **objprops) :
		obj.update(objprops)
		for key, val in obj.items() :
			if isinstance(val, dict) :
				obj[key] = Struct(val)
		super(Struct, self).__init__(obj)

	def __getattribute__(self, attr) :
		if attr[0] == "_" :
			return object.__getattribute__(self, attr[1:])
		else :
			return self[attr]

	def __setattr__(self, attr, val) :
		if attr[0] == "_" :
			object.__setattr__(self, attr[1:], val)
		else :
			self[attr] = val

	def __iter__(self) :
		for key, val in self._items() :
			yield (key, val)


class Timer(object) :
	
	def __init__(self, func = None) :
		self.func = func
	
	def __call__(self, *args, **kwargs) :
		if self.func :
			self.__enter__()
			res = self.func(*args, **kwargs)
			self.__exit__()
			return res
		else :
			raise TypeError("'Timer' object is not used as a decorator and therefore not callable")
	
	def __enter__(self, *args, **kwargs) :
		self.t0 = time.time()
	
	def __exit__(self, *args, **kwargs) :
		dt = time.time() - self.t0
		print "=> Execution{func} took {time:.6} seconds".format(func = " of {0}()".format(self.func.__name__) if self.func else "", time = dt)
