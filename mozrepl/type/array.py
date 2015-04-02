#!/usr/bin/env python
#-*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import, division, print_function
#from ufp.terminal.debug import print_ as debug

from .object import Object

class Array(Object):
	"""
	javascript array에 대한 인터페이스를 제공합니다.
	
	__len__, __iter__ 메소드가 구현되어 있습니다.
	
	.. todo:: __iter__ 메소드 사용시, 속성을 JSON.stringify 함수로 json으로 만들어두고 {type, value}, 가져올 수 있는 기본 타입(string, number, bool 등)은 그대로 둔다. 참조값이 존재하는 Object타입은 value에 참조값을 만들어 둔다.
	
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
		buffer = '{reference}.length;'.format(
			reference = self
			)
		return self._repl.execute(buffer) 
	
	def __iter__(self):
		"""
		javascript Object에 iterator하게 접근합니다.
		
		:yield: value; 0 ~ 마지막 값까지 yield합니다.
		"""
		for index in range(len(self)):
			buffer = '{reference}[{index}];'.format(
				reference = self, 
				index = index
				)
			yield self._repl.execute(buffer)
		raise StopIteration
	