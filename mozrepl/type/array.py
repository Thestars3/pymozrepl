#!/usr/bin/env python
#-*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import, division, print_function
#from ufp.terminal.debug import print_ as debug

from .object import Object

class Array(Object):
	"""
	javascript array에 대한 인터페이스를 제공합니다.
	
	__len__, __iter__ 메소드가 구현되어 있습니다.
	
	사용 예는 다음과 같습니다.
	
	.. code-block:: python
	
		>>> import mozrepl
		>>> repl = mozrepl.Mozrepl()
		>>> array = repl.execute('[1,2,3,4,5,10]')
		>>> len(array) # __len__
		6
		>>> list(array) # __iter__
		[1, 2, 3, 4, 5, 10]
	
	"""
	def __init__(self, repl, uuid):
		super(Array, self).__init__(repl, uuid)
	
	def __len__(self):
		return self._repl.execute('{reference}.length'.format(reference=self)) 
	
	def __iter__(self):
		max = len(self)
		for index in range(max):
			yield self._repl.execute('{reference}[{index}]'.format(reference=self, index=index))
		raise StopIteration
	