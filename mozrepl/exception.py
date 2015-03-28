#!/usr/bin/env python
#-*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import, division, print_function
import exceptions

class Exception(exceptions.Exception):
	"""
	mozrepl Firefox Add-on에서 반환한 오류.
	
	typeName, summary, details 멤버에 접근하여 오류에 대해 상세히 알 수 있습니다.
	"""
	def __init__(self, typeName, summary, details=''):
		self.typeName = typeName
		self.summary = summary
		self.details = details
	
	def __str__(self):
		return '{0}: {1}'.format(self.typeName, self.summary)
