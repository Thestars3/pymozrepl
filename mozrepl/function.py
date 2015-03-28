#!/usr/bin/env python
#-*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import, division, print_function
import itertools

class Function():
	def __init__(self, repl, uuid):
		self._uuid = uuid
		self._repl = repl
	
	def __call__(self, *args, **kwargs):
		"""
		오직 문자열과 숫자만 전달 가능.
		
		:todo: 함수 및 오브젝트를 전달 가능하도록 만들기. 문자열에 \'문자가 포함되어 있을 경우 문제가 발생 할 수 있음. 콰우팅 시켜주기.
		"""
		buffer = '{0}.ref.{1}'.format(self._repl._baseVarname, self._uuid)
		v = list()
		for i in itertools.chain(args, kwargs.values()):
			if isinstance(i, int):
				v.append(str(i))
			elif isinstance(i, unicode):
				v.append(repr(str(i)))
		buffer = '{0}({1})'.format(buffer, ','.join(v))
		return self._repl.execute(buffer)
		