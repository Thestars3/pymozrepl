#!/usr/bin/env python
#-*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import, division, print_function

class Object(object):
	"""
	..
	   자바 스크립트의 오브젝트는 파이썬의 사전과 유사하다.
	   자바 스크립트의 오브젝트의 각 요소는 모두 개별 요소로 존재한다.
	   만약, Mozrepl.execute 메소드를 통해 오브젝트를 반환받은 경우, 이 오브젝트는 참조값으로 존재하는가? 아니면, 복제되는가?
	   참조값으로 생각한다면, 이 값에 접근 할때 마다 접속후 연산할 필요성이 있다. 그러나, 이렇게 하면, 속도가 지연된다.
	   
	"""
	def __init__(self):
		pass
	
	
	