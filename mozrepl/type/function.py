#!/usr/bin/env python
#-*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import, division, print_function
import itertools

from .object import Object

class Function(Object):
	"""
	javascript function에 대한 인터페이스를 제공합니다.
	
	사용 예는 다음과 같습니다.
	
	.. code-block:: python
	
		>>> import mozrepl
		>>> repl = mozrepl.Mozrepl()
		>>> func = repl.execute('(function(){ return "mozrepl"; })') #__call__
		>>> func()
		u'mozrepl'
		>>> func = repl.execute('repl').home() #__call__
		[object ChromeWindow] - {0: {...}, 1: {...}, 2: {...}, 3: {...}, 4: {...}, 5: {...}, 6: {...}, ...}
	
	"""
	def __init__(self, repl, uuid):
		super(Function, self).__init__(repl, uuid)
	
	def __repr__(self):
		return 'function() {...}'
	
	def __call__(self, *args):
		"""
		javascript Function object를 실행합니다.
		
		입력하는 각 인자는 :py:func:`~mozrepl.util.convertToJs` 함수에서 허용하는 형식을 준수해야 합니다.
		"""
		buffer = itertools.chain(args)
		buffer = map(convertToJs, buffer)
		buffer = '{reference}({args})'.format(reference=self, args=', '.join(buffer))
		return self._repl.execute(buffer)
	

from ..util import convertToJs
