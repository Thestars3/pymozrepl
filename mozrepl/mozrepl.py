#!/usr/bin/env python
#-*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import, division, print_function
import sys
import re
import telnetlib
import uuid

from . import Exception as MozException
from .type import Object, Function

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
		
		self._baseVarname = '__pymozrepl_' + uuid.uuid4().hex
		self.execute("""\
			var %(_baseVarname)s = Object(); 
			%(_baseVarname)s.ref = Object();
			""" % vars(self),
			'noreturn')
		pass
	
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
	
	def _convRtype(self, respon):
		"""
		undefined, null값은 반환받는 결과가 존재하지 않아, 자동으로 None값이 리턴되었음. 따라서, 처리에서 생략함.
		array는 오브젝트이므로, 별도의 처리를 하지 않음. 별도로 처리한다면, 값을 copy하는 객체를 만들어 처리 할 것.
		"""
		#boolean
		if respon in ['false', 'true']:
			return respon == 'true'
		
		#Number - int
		if re.match(r'\d+$', respon):
			return int(respon)
		
		#Number - float
		if re.match(r'\d+\.\d+$', respon):
			return float(respon)
		
		#string
		match = re.match(r'"(.*)"$', respon)
		if match:
			buffer = match.group(1)
			#buffer = re.sub(r'\\(.)', r'\1', buffer) # repl.js 에서 별도의 콰우팅을 수행하고 있지 않았음.
			return buffer
		
		type = self.execute("typeof {0}.lastExecVar".format(self._baseVarname), 'nolastcmd')
		
		#object
		if type == 'object':
			uuid_ = '_' + uuid.uuid4().hex
			self.execute('{0}.ref.{1} = {0}.lastExecVar'.format(self._baseVarname, uuid_), 'noreturn')
			return Object(self, uuid_)
		
		#function
		if type == 'function':
			uuid_ = '_' + uuid.uuid4().hex
			self.execute('{0}.ref.{1} = {0}.lastExecVar'.format(self._baseVarname, uuid_), 'noreturn')
			return Function(self, uuid_)
		
		return respon
	
	def execute(self, command, type='parse'):
		"""
		명령을 실행합니다.
		
		:param command: 명령.
		:type command: unicode
		:param type: \n
			parse : 반환받은 결과를 파싱함.\n
			repr : 반환받은 결과를 그대로 반환.\n
			noreturn : 반환받는 결과가 없음(for문을 쓰는 등, 반환결과가 없는 경우 발생하는 문법 오류를 회피하기 위한 설정).\n
			nolastcmd : 마지막으로 실행한 변수의 값을 저장하는 기능을 비활성화시킴.
		:raise mozrepl.Exception: mozrepl Firefox Add-on에서 오류를 던질 경우.
		:returns: int : mozrepl Firefox Add-on에서 반환받은 값이 정수인 경우.
		:returns: float : mozrepl Firefox Add-on에서 반환받은 값이 실수인 경우.
		:returns: unicode : mozrepl Firefox Add-on에서 반환받은 값이 문자열인 경우.
		:returns: unicode : mozrepl Firefox Add-on에서 반환받은 값을 분석 할 수 없는 경우 또는 type이 repr로  설정된 경우에 응답 받은 값을 그대로 반환합니다.
		:returns: bool : mozrepl Firefox Add-on에서 반환받은 값이 진리형인 경우.
		"""
		if type in ['noreturn', 'nolastcmd']:
			self._telnet.write("{0};\n".format(command).encode('utf8')) #전송
		else:
			self._telnet.write("{0}.lastExecVar = {1};\n".format(self._baseVarname, command).encode('utf8')) #전송
		respon = self._telnet.read_until(self.prompt).decode('utf8') #수신
		
		#아무 응답도 없을 경우 None을 반환
		if re.search('^ %(prompt)s$' % vars(self), respon):
			return None
		
		#응답이 존재하는 경우 응답받은 문자열에서 불필요한 문자열을 제거.
		respon = re.sub('^ ', '', respon) #응답된 문자열의 앞 공백 제거
		respon = re.sub(r'\n%(prompt)s$' % vars(self), '', respon, re.UNICODE) #입력 프롬프트 제거
		
		#오류일 경우 예외를 던짐.
		match = re.match(r'\!{3} (.+?): (.+?)\n\nDetails:(.*?)\n\n$', respon)
		if match:
			typeName = match.group(1)
			summary = match.group(2)
			details = match.group(3)
			raise MozException(typeName, summary, details)
		
		#응답받는 결과가 없는 경우
		if type == 'noreturn':
			return None
		
		#그대로 반환
		if type == 'repr':
			return respon
		
		#변환
		return self._convRtype(respon)
	