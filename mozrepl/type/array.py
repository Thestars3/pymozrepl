#!/usr/bin/env python
#-*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import, division, print_function
#from ufp.terminal.debug import print_ as debug

from .object import Object

class Array(Object):
	def __init__(self, repl, uuid):
		super(Array, self).__init__(repl, uuid)
	
	def __iter__(self):
		max = self._repl.execute('{reference}.length'.format(reference=self.reference))
		for index in range(max):
			yield self._repl.execute('{reference}[{index}]'.format(reference=self.reference, index=index))
		raise StopIteration
	