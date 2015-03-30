#!/usr/bin/env python
#-*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import, division, print_function
import exceptions

class Exception(exceptions.Exception):
	"""
	mozrepl Firefox Add-on에서 반환한 오류에 대한 정보를 담는 클래스.
	"""
	def __init__(self, typeName, summary='', details=''):
		self._typeName = typeName
		self._summary = summary
		self._details = details
	
	@property
	def typeName(self):
		"""타입 이름"""
		return self._typeName
	
	@property
	def summary(self):
		"""요약"""
		return self._summary
	
	@property
	def details(self):
		"""상세 설명"""
		return self._details
	
	def __str__(self):
		return '{typeName}: {summary}'.format(typeName=self.typeName, summary=self.summary)
	