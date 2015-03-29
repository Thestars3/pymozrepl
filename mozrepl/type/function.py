#!/usr/bin/env python
#-*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import, division, print_function
import itertools

from . import Object

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
		오직 문자열과 숫자만 전달 가능.
		
		:todo: 함수 및 오브젝트를 전달 가능하도록 만들기. 문자열에 \'문자가 포함되어 있을 경우 문제가 발생 할 수 있음. 콰우팅 시켜주기.
			None 타입의 경우 null로 처리하도록 함.
			+ mozrepl.type.Function에서 발생하던 'TypeError: context is undefined' 오류를 수정. [`tb69wn6127`_]
		"""
		v = list()
		for i in itertools.chain(args, kwargs.values()):
			if isinstance(i, int):
				v.append(str(i))
			elif isinstance(i, unicode):
				v.append(repr(str(i)))
		buffer = '{0}({1})'.format(self.reference, ','.join(v))
		print(buffer)
		return self._repl.execute(buffer)
	