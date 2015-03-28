#!/usr/bin/env python
#-*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import, division, print_function
import sys
import re
import telnetlib

from .exception import Exception as MozException
#from .object import Object

DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 4242

class Mozrepl(object):
	"""
	모질라 파이어폭스에서 REPL 확장 프로그램을 실행한 뒤 사용하십시오.
	
	with 구문을 지원합니다.
	
	..
	   https://github.com/bard/mozrepl/wiki/Pyrepl bard/mozrepl Wiki
	"""
	_RE_PROMPT = re.compile(r'^repl\d*>', re.MULTILINE)
	
	def __init__(self, port=DEFAULT_PORT, host=DEFAULT_HOST):
		"""
		mozrepl Firefox Add-on과 연결합니다.
		
		:param port: mozrepl Firefox Add-on의 포트.
		:param port: mozrepl Firefox Add-on의 호스트.
		"""
		self.connect(port, host)
	
	def connect(self, port=None, host=None):
		"""
		mozrepl Firefox Add-on과 연결합니다.
		
		:param port: mozrepl Firefox Add-on의 포트. 생략시, 기존 값을 사용합니다.
		:param port: mozrepl Firefox Add-on의 호스트. 생략시, 기존 값을 사용합니다.
		"""
		if port is not None:
			self.port = port
		if host is not None:
			self.host = host
		self._telnet = telnetlib.Telnet(self.host, self.port)
		match = self._telnet.expect([self._RE_PROMPT], 10)[1]
		self.prompt = match.group(0)
	
	def __enter__(self):
		return self
	
	def disconnect(self):
		"""
		mozrepl Firefox Add-on과의 연결을 끊습니다.
		"""
		self.prompt = None
		self._telnet.close()
		del self._telnet
	
	def __exit__(self, type, value, traceback):
		self.disconnect()
	
	def for_(self, command, var):
		"""
		command의 실행 결과들을 var에 담습니다.
		yield되는 값은 무의미 합니다.
		"""
		self.console('let iter = %(command)s' % locals())
		length = self.console('iter.length')
		for i in range(length):
			self.console('let %(var)s = iter[%(i)s]' % locals())
			yield i
	
	def execute(self, command):
		"""
		명령을 실행합니다.
		
		:param command: 명령.
		:type command: unicode
		:raise mozrepl.Exception: mozrepl Firefox Add-on에서 오류를 던질 경우.
		:returns: int : mozrepl Firefox Add-on에서 반환받은 값이 정수인 경우.
		:returns: unicode : mozrepl Firefox Add-on에서 반환받은 값이 문자열인 경우.
		:returns: unicode : mozrepl Firefox Add-on에서 반환받은 값을 분석 할 수 없는 경우 응답 받은 값을 그대로 반환합니다.
		:returns: bool : mozrepl Firefox Add-on에서 반환받은 값이 진리형인 경우.
		"""
		self._telnet.write(command.encode('utf8') + b';\n') #전송
		respon = self._telnet.read_until(self.prompt).decode('utf8') #수신
		
		#아무 응답도 없을 경우 None을 반환
		if re.search('^ %(prompt)s$' % vars(self), respon):
			return None
		
		respon = re.sub('^ ', '', respon) #응답된 문자열의 앞 공백 제거
		respon = re.sub(r'\n%(prompt)s$' % vars(self), '', respon, re.UNICODE) #입력 프롬프트 제거
		
		#오류일 경우 예외를 던짐.
		match = re.search(r'^\!{3} (.+?): (.+?)\n\nDetails:(.*?)\n\n$', respon)
		if match:
			typeName = match.group(1)
			summary = match.group(2)
			details = match.group(3)
			raise MozException(typeName, summary, details)
		
		#bool
		if respon in ['false', 'true']:
			return respon == 'true'
		
		#int
		if re.match(r'\d+$', respon):
			return int(respon)
		
		#object
		match = re.match('\[object (.+?)\]', respon)
		if match:
			#Object()
			return respon
		
		#string
		match = re.match(r'^"(.*)"$', respon)
		if match:
			buffer = match.group(1)
			buffer = re.sub(r'\\(.)', r'\1', buffer)
			return buffer
		
		return respon
