#!/usr/bin/env python
#-*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import, division, print_function
import itertools

from .object import Object
from ..util import convertToJs

class Function(Object):
	"""
	javascript function에 대한 인터페이스를 제공합니다.
	"""
	def __init__(self, repl, uuid):
		super(Function, self).__init__(repl, uuid)
	
	def __repr__(self):
		return 'function() {...}'
	
	def __call__(self, *args, **kwargs):
		"""
		javascript Function object를 실행합니다.
		
		입력하는 각 인자는 :py:func:`~mozrepl.util.convertToJs` 함수에서 허용하는 형식을 준수해야 합니다.
		"""
		buffer = itertools.chain(args, kwargs.values())
		buffer = map(convertToJs, buffer)
		buffer = '{reference}({args})'.format(reference=self.reference, args=', '.join(buffer))
		return self._repl.execute(buffer)
	