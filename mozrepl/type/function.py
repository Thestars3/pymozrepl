#!/usr/bin/env python
#-*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import, division, print_function
import itertools

from .object import Object

class Function(Object):
	"""
	자바스크립트 함수.
	"""
	def __init__(self, repl, uuid):
		super(Function, self).__init__(repl, uuid)
	
	def __repr__(self):
		return 'function() {...}'
	
	def __call__(self, *args, **kwargs):
		"""
		내부에서 :py:function:`~mozrepl.util.convertToJs` 함수를 호출하여 처리합니다. 입력하는 각 인자는 이 함수에서 허용하는 형식을 준수해야 합니다.
		"""
		v = list()
		for i in itertools.chain(args, kwargs.values()):
			type
		buffer = '{reference}({args})'.format(reference=self.reference, args=','.join(v))
		return self._repl.execute(buffer)
	