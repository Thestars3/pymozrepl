#!/usr/bin/env python
#-*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import, division, print_function

class Raw():
	"""
	자바스크립트 코드를 담는 클래스.
	
	이 클래스로 생성된 코드는 :py:func:`~mozrepl.util.convertToJs` 함수에 의해 변환되지 않고, 입력된 그대로 전달되게 됩니다.
	
	:param code: 자바스크립트 코드.
	:type code: unicode
	"""
	def __init__(self, code):
		self.code = code
	
	def __unicode__(self):
		return self.code
		