#!/usr/bin/env python
#-*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import, division, print_function
import exceptions
#from ufp.terminal.debug import print_ as debug

class Exception(exceptions.Exception):
	"""
	mozrepl Firefox Add-on에서 반환한 오류에 대한 정보를 담는 클래스.
	
	javascript Error 객체를 참조 하듯이 속성을 참조하십시오. 단, 메소드에 대한 참조는 지원하지 않습니다.
	
	만약, 현재 객체에 존재하고 있는 이름과 같은 이름의 javascript object 속성에 접근하려면, __getitem__ 메소드를 사용하십시오.
	
	특정 속성이 존재하는가를 검사하려면 __contains__ 메소드를 사용하십시오.
	
	.. todo:: typeName, details 속성을 2.x 버전대에서 제거 할 것.
	"""
	def __init__(self, error):
		self._error = error
		self.typeName = self._error.get('name', '')
		self.details = self._error.get('message', '')
		message = self._error.get('message', '')
	
	def __contains__(self, name):
		if name in self._error:
			return True
		return False
	
	def __getattr__(self, name):
		if name in self._error:
			return self._error[name]
		raise AttributeError(b"{name} 속성이 존재하지 않습니다.".format(name=repr(name)))
	
	def __getitem__(self, key):
		if key in self._error:
			return self._error[key]
		raise KeyError(b"{key} 키가 존재하지 않습니다.".format(key=repr(key)))
	
	def __str__(self):
		msg = unicode()
		if 'name' in self._error:
			msg += '{name}: '.format(name=self._error['name'])
		msg += self._error['message']
		return msg
	
