#!/usr/bin/env python
#-*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import, division, print_function
import sys
import re
import telnetlib
import uuid
import urlparse
import urllib
import tempfile
#from ufp.terminal.debug import print_ as debug

from .exception import Exception as MozException
from .type import Object, Function, Array
from .util import convertToJs

DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 4242

class Mozrepl(object):
	"""
	Firefox MozREPL Add-on에 대한 인터페이스를 제공하는 클래스.
	
	with 구문을 지원합니다.
	
	..
	   https://github.com/bard/mozrepl/wiki/Pyrepl bard/mozrepl Wiki
	
	:param port: mozrepl Firefox Add-on의 포트.
	:type port: int
	:param host: mozrepl Firefox Add-on의 호스트.
	:type host: unicode
	"""
	_RE_PROMPT = re.compile(r'^repl\d*>', re.MULTILINE)
	
	def __init__(self, port=DEFAULT_PORT, host=DEFAULT_HOST):
		"""
		mozrepl Firefox Add-on과 연결합니다.
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
		
		self._baseVarname = '__pymozrepl_{0}'.format(uuid.uuid4().hex)
		
		self._rawExecute("""\
				var {baseVar} = {{
					'ref': Object(),
					'buffer': null,
					'lastCmdValue': null
				}}
				""".format(baseVar=self._baseVarname)
			)
		pass
	
	def __repr__(self):
		return 'Mozrepl(port={port}, host={host})'.format(port=repr(self.port), host=repr(self.host))
	
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
	
	def _rawExecute(self, command):
		"""
		명령을 실행합니다. 
		
		execute 메소드와 달리 명령을 분석하지 않고, Firefox MozREPL Add-on에서 반환받은 문자열을 그대로 반환합니다.
		
		:param command: 명령.
		:type command: unicode
		:return: Firefox MozREPL Add-on에서 반환받은 문자열을 정리한 문자열.
		:return: Firefox MozREPL Add-on에서 응답이 없는 경우 None을 반환.
		:rtype: unicode
		"""
		self._telnet.write('{command};\n'.format(command=command).encode('utf8')) #전송
		respon = self._telnet.read_until(self.prompt).decode('utf8') #수신
		
		#아무 응답도 없을 경우 None을 반환
		if re.search('^ %(prompt)s$' % vars(self), respon):
			return None
		
		#응답이 존재하는 경우 응답받은 문자열에서 불필요한 문자열을 제거.
		respon = re.sub('^ ', '', respon) #응답된 문자열의 앞 공백 제거
		respon = re.sub(r'\n%(prompt)s$' % vars(self), '', respon, re.UNICODE) #입력 프롬프트 제거
		
		#오류일 경우 예외를 던짐.
		match = re.match(r'!{3} \[\S+? (?P<typeNmae>\S+?)\]\n\nDetails:\n(?P<details>.*?)\n', respon, re.DOTALL) \
			or re.match(r'!{3} (?P<typeNmae>\S+?): (?P<summary>.+?)\n\nDetails:\n(?P<details>.*?)\n$', respon, re.DOTALL) \
			or re.match(r'!{3} \[Exception\.{3} (?P<summary>"Component returned failure code: 0x8000ffff \((?P<typeNmae>\S+?)\).*?)\]\n\nDetails:\n(?P<details>.*?)\n$', respon, re.DOTALL) \
			or re.match(r'!{3} \[Exception\.{3} (?P<summary>.*?)\]\n\nDetails:\n(?P<details>.*?)\n$', respon, re.DOTALL) \
			or re.match(r'!{3} (?P<summary>.*)\nDetails:\n(?P<details>.*?)\n$', respon, re.DOTALL) \
			or re.match(r'!{3} (?P<summary>.*)$', respon, re.DOTALL)
		if match:
			groupdict = match.groupdict()
			typeName = groupdict.get('typeNmae', '')
			summary = groupdict.get('summary', '')
			details = groupdict.get('details', '')
			raise MozException(typeName, summary, details)
		
		return respon
	
	def __del__(self):
		self._rawExecute("""
			delete {baseVar}.ref
			delete {baseVar}.buffer
			delete {baseVar}
			""".format(baseVar=self._baseVarname)
			)
		pass
	
	def execute(self, command):
		"""
		명령을 실행합니다.
		
		:param command: 명령.
		:type command: unicode
		:raise mozrepl.Exception: mozrepl Firefox Add-on에서 오류를 던질 경우.
		:returns: int : mozrepl Firefox Add-on에서 반환받은 값이 정수인 경우.
		:returns: float : mozrepl Firefox Add-on에서 반환받은 값이 실수인 경우.
		:returns: unicode : mozrepl Firefox Add-on에서 반환받은 값이 문자열인 경우.
		:returns: :py:class:`~mozrepl.type.Object` : mozrepl Firefox Add-on에서 반환받은 값이 object인 경우.
		:returns: :py:class:`~mozrepl.type.Array` : mozrepl Firefox Add-on에서 반환받은 값이 array인 경우.
		:returns: :py:class:`~mozrepl.type.Function` : mozrepl Firefox Add-on에서 반환받은 값이 function인 경우.
		:returns: unicode : mozrepl Firefox Add-on에서 반환받은 값을 분석 할 수 없는 경우 또는 type이 repr로  설정된 경우에 응답 받은 값을 그대로 반환합니다.
		:returns: bool : mozrepl Firefox Add-on에서 반환받은 값이 진리형인 경우.
		"""
		#명령을 실행
		with tempfile.NamedTemporaryFile('wb', prefix='.tmp_pymozrepl_', suffix='.js') as tempFile:
			tempFile.write(command.encode('UTF-8'))
			tempFile.flush()
			scriptUrl = urlparse.urljoin('file:', urllib.pathname2url(tempFile.name.encode('UTF-8')))
			respon = self._rawExecute('{baseVar}.lastCmdValue = repl.loader.loadSubScript("{scriptUrl}", this, "UTF-8")'.format(scriptUrl=scriptUrl, baseVar=self._baseVarname)) #명령을 mozrepl 서버에 전송
		
		#응답받은 결과가 없으면 그대로 반환
		if respon is None:
			return None
		
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
			return match.group(1)
		
		#function
		if respon == 'function() {...}':
			uuid_ = unicode(uuid.uuid4())
			match = re.search('(\S+?)(\.[^.]+|\[.+?\])\s*$', command)
			self._rawExecute('{baseVar}.ref["{uuid}"] = {baseVar}.lastCmdValue'.format(baseVar=self._baseVarname, uuid=uuid_))
			return Function(self, uuid_)
		
		#타입 분석.
		type = self.execute("""{baseVar}.buffer = {baseVar}.lastCmdValue; typeof {baseVar}.lastCmdValue""".format(baseVar=self._baseVarname))
		
		#array, object
		if type == 'object':
			uuid_ = unicode(uuid.uuid4())
			self._rawExecute('{baseVar}.ref["{uuid}"] = {baseVar}.buffer'.format(baseVar=self._baseVarname, uuid=uuid_))
			
			#array
			if self.execute('Array.isArray({baseVar}.buffer)'.format(baseVar=self._baseVarname)):
				return Array(self, uuid_)
			
			#object
			return Object(self, uuid_)
		
		return respon
	