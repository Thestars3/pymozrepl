#!/usr/bin/env python
#-*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import, division, print_function
import sys
import re
import telnetlib
import uuid
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
		self._rawExecute("""\
			{baseVar} = Object(); 
			{baseVar}.ref = Object();
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
	
	def _convertMozreplResonToPyStruct(self, respon, command):
		"""
		undefined, null값은 반환받는 결과가 존재하지 않아, 자동으로 None값이 리턴되었음. 따라서, 처리에서 생략함.
		array는 오브젝트이므로, 별도의 처리를 하지 않음. 별도로 처리한다면, 값을 copy하는 객체를 만들어 처리 할 것.
		
		:todo: function 타입 처리시, 부모 오브젝트를 찾아야 한다. 함수에서 부모 오브젝트를 찾는건 불가능하므로, 입력받은 명령을 분석하여 부모를 찾아야 한다. 이를 좀더 매끄럽게 해야한다.
		:todo: object 타입 처리시, 부모 오브젝트를 찾아야 묶어야 한다.
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
		
		#function
		if respon == 'function() {...}':
			uuid_ = unicode(uuid.uuid4())
			match = re.search('(\S+?)(\.[^.]+|\[.+?\])\s*$', command)
			if match:
				context = match.group(1)
			else:
				context = 'this'
			self._rawExecute('{baseVar}.ref["{uuid}"] = {baseVar}.lastExecVar.bind({context})'.format(baseVar=self._baseVarname, uuid=uuid_, context=context))
			return Function(self, uuid_)
		
		type = self.execute("typeof {baseVar}.lastExecVar".format(baseVar=self._baseVarname))
		
		#array
		if type == 'object' and self.execute('Array.isArray({baseVar}.lastExecVar)'.format(baseVar=self._baseVarname)):
			uuid_ = unicode(uuid.uuid4())
			#self.execute('{baseVar}.ref["{uuid}"] = function(){{ with({context}){{ return {context}.lastExecVar; }}; }}'.format(baseVar=self._baseVarname, uuid=uuid_, context=context), 'noreturn')
			self._rawExecute('{baseVar}.ref["{uuid}"] = {baseVar}.lastExecVar'.format(baseVar=self._baseVarname, uuid=uuid_))
			return Array(self, uuid_)
		
		#object
		if type == 'object':
			uuid_ = unicode(uuid.uuid4())
			#self.execute('{baseVar}.ref["{uuid}"] = function(){{ with({context}){{ return {baseVar}.lastExecVar; }}; }}'.format(baseVar=self._baseVarname, uuid=uuid_, context=context), 'noreturn')
			self._rawExecute('{baseVar}.ref["{uuid}"] = {baseVar}.lastExecVar'.format(baseVar=self._baseVarname, uuid=uuid_))
			return Object(self, uuid_)
		
		return respon
	
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
		#전송
		buffer = "{command};\n".format(command=command)
		buffer = buffer.encode('utf8')
		self._telnet.write(buffer)
		
		#수신
		buffer = self._telnet.read_until(self.prompt)
		respon = buffer.decode('utf8')
		
		#아무 응답도 없을 경우 None을 반환
		if re.search('^ %(prompt)s$' % vars(self), respon):
			return None
		
		#응답이 존재하는 경우 응답받은 문자열에서 불필요한 문자열을 제거.
		respon = re.sub('^ ', '', respon) #응답된 문자열의 앞 공백 제거
		respon = re.sub(r'\n%(prompt)s$' % vars(self), '', respon, re.UNICODE) #입력 프롬프트 제거
		
		#오류일 경우 예외를 던짐.
		match = re.match(r'!{3} \[\S+? (?P<typeNmae>\S+?)\]\n\nDetails:(?P<details>.*?)\n\n', respon) or re.match(r'!{3} (?P<typeNmae>\S+?): (?P<summary>.+?)\n\nDetails:(?P<details>.*?)\n\n$', respon)
		if match:
			groupdict = match.groupdict()
			groupdict.setdefault('summary', '')
			typeName = groupdict['typeNmae']
			summary = groupdict['summary']
			details = groupdict['details']
			raise MozException(typeName, summary, details)
		
		return respon
	
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
		#명령이 결과를 반환하는가를 검사
		isHaveRespon = True
		command = command.strip()
		if re.match(r'(//.*$|/\*.*?\*/)?\s*(for|while)\s+', command):
			isHaveRespon = False
		
		#명령을 mozrepl 서버에 전송
		if isHaveRespon:
			buffer = "{baseVar}.lastExecVar = {command}".format(baseVar=self._baseVarname, command=command)
		else:
			buffer = command
		respon = self._rawExecute(buffer)
		
		if respon is None:
			return None
		
		if isHaveRespon:
			return self._convertMozreplResonToPyStruct(respon, command) #변환
		pass
	