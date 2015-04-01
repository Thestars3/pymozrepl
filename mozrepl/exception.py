#!/usr/bin/env python
#-*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import, division, print_function
import exceptions
#from ufp.terminal.debug import print_ as debug

class Exception(exceptions.Exception):
	"""
	mozrepl Firefox Add-on에서 반환한 오류에 대한 정보를 담는 클래스.
	
	javascript Error 객체를 참조 하듯이 속성을 참조하십시오. 단, 메소드에 대한 참조는 지원하지 않습니다.
	
	.. todo:: typeName, details 속성을 2.x 버전대에서 제거 할 것.
	"""
	def __init__(self, error):
		self._error = error
		self.typeName = self._error.get('name', '')
		self.details = ''
	
	def __getattr__(self, key):
		if key in self._error:
			return self._error[key]
	
	def __str__(self):
		msg = unicode()
		if self.name:
			msg += '{name}: '.format(name=self.name)
		msg += self.message
		return msg
	