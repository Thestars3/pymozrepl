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
import base64
import json
#from ufp.terminal.debug import print_ as debug

from .exception import Exception as MozException
from .type import Object, Function, Array

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
	DEFAULT_HOST = '127.0.0.1'
	DEFAULT_PORT = 4242
	
	def __init__(self, port=DEFAULT_PORT, host=DEFAULT_HOST):
		"""
		mozrepl Firefox Add-on과 연결합니다.
		"""
		self.connect(port, host)
		
		self._baseVarname = '__pymozrepl_{0}'.format(uuid.uuid4().hex)
		
		buffer = """var {baseVar} = {{ 'ref': {{}}, 'context': {{}}, 'modules': {{}} }}; (function(){{ let {{ Loader }} = Components.utils.import("resource://gre/modules/commonjs/toolkit/loader.js", {{}}); let loader = Loader.Loader({{ paths: {{ "sdk/": "resource://gre/modules/commonjs/sdk/", "": "resource://gre/modules/commonjs/" }}, modules: {{ "toolkit/loader": Loader, "@test/options": {{}} }}, resolve: function(id, base) {{ if ( id == "chrome" || id.startsWith("@") ) {{ return id; }}; return Loader.resolve(id, base); }} }}); let requirer = Loader.Module("main", "chrome://URItoRequire"); let require = Loader.Require(loader, requirer); {baseVar}.modules.require = require; }}()); (function(){{ {baseVar}.modules.base64 = {baseVar}.modules.require('sdk/base64'); }}()); null;""".format(
			baseVar=self._baseVarname
			)
		self._rawExecute(buffer)
	
	def connect(self, port=None, host=None):
		"""
		mozrepl Firefox Add-on과 연결합니다.
		
		연결 대상은 최초 연결된 대상과 같아야 합니다.
		
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
		#전송
		buffer = """try {{ {command}; }} catch (e) {{ (function() {{ let robj = {{ 'exception': {{}} }}; Object.getOwnPropertyNames(e).forEach(function (key) {{ robj.exception[key] = e[key]; }}, e); let buffer; buffer = JSON.stringify(robj); buffer = window.btoa(unescape(encodeURIComponent(buffer))); return buffer; }}()) }};""".format(
			command = command,
			baseVar = self._baseVarname
			)
		self._telnet.write(buffer.encode('UTF-8'))
		
		respon = self._telnet.read_until(self.prompt) #수신
		
		#응답이 존재하는 경우 응답받은 문자열에서 불필요한 문자열을 제거.
		respon = re.sub('^ (\.{4}> )*', '', respon) #응답된 문자열의 앞 공백 제거
		respon = re.sub(r'\s*%(prompt)s$' % vars(self), '', respon, re.UNICODE) #입력 프롬프트 제거
		
		#아무 응답도 없을 경우 None을 반환
		if not respon:
			return None
		
		respon = respon[1:-1] # 쌍따옴표를 제거
		
		respon = base64.decodestring(respon).decode('UTF-8')
		respon = json.loads(respon) #받은 내용을 파싱.
		
		#오류일 경우 예외를 던짐.
		if 'exception' in respon:
			raise MozException(respon['exception'])
		
		return respon
	
	def __del__(self):
		buffer = """delete {baseVar}; null;""".format(baseVar=self._baseVarname)
		self._rawExecute(buffer)
	
	def execute(self, command):
		"""
		명령을 실행합니다.
		
		.. attention:: 오브젝트의 메소드를 사용할때, 'repl.execute("repl.home")()'과 같이 함수의 메소드를 바로 반환 받은 뒤 사용 할 수 없습니다. 이와 같은 방식으로 사용하려면, 'repl.execute("repl.home.call")(Raw("repl"))'와 같이 호출 오브젝트를 명시적으로 넘겨주거나, 'repl.execute("repl").home()'과 같이 pymozrepl의 자동 바인딩 기능을 사용하십시오.
		.. attention:: 하나의 pymozrepl 객체는 독립된 하나의 문맥을 가집니다. 이 문맥은 Firefox mozrepl에서 제공하는 현재 문맥과는 다르다는 점을 주의하십시오.
		.. todo:: 명령 응답 중에 prompt가 섞여서 일부 내용은 완전히 받지 못 할 수 있다. 또, -inf나 long 따위의 값은 처리를 하지 못하는 문제가 있다. 이런 문제를 해결하기 위해, 응답을 json으로 만들고 파일 입출력을 통해 반환받도록 한다.
		
		:param command: 명령.
		:type command: unicode
		:raise mozrepl.Exception: mozrepl Firefox Add-on에서 오류를 던질 경우.
		:returns: :py:class:`~mozrepl.type.Object` : mozrepl Firefox Add-on에서 반환받은 값이 object인 경우.
		:returns: :py:class:`~mozrepl.type.Array` : mozrepl Firefox Add-on에서 반환받은 값이 array인 경우.
		:returns: :py:class:`~mozrepl.type.Function` : mozrepl Firefox Add-on에서 반환받은 값이 function인 경우.
		:returns: 그 외에 string, number, bool 등의 기본값은 python에서 대응되는 적절한 기본 타입(int, bool, unicode 등)으로 변환하여 돌려줍니다.
		"""
		#명령을 실행
		with tempfile.NamedTemporaryFile('wb', prefix='.tmp_pymozrepl_', suffix='.js') as scriptFile:
			#명령 기록
			scriptFile.write(command.encode('UTF-8'))
			scriptFile.flush()
			
			#기록된 명령 파일의 주소를 생성
			buffer = scriptFile.name.encode('UTF-8')
			buffer = urllib.pathname2url(buffer)
			scriptUrl = urlparse.urljoin('file:', buffer)
			
			#명령을 mozrepl 서버에 전송
			buffer = """(function(){{ let robj = {{}}; let lastCmdValue = repl.loader.loadSubScript("{scriptUrl}", {baseVar}.context, "UTF-8"); robj.type = typeof lastCmdValue; if ( robj.type == 'object' ) {{ if ( Array.isArray(lastCmdValue) ) {{ robj.type = 'array'; }}; {baseVar}.ref['{refUuid}'] = lastCmdValue; robj.refUuid = '{refUuid}'; }} else {{ robj.value = lastCmdValue; }}; let buffer; buffer = JSON.stringify(robj); buffer = {baseVar}.modules.base64.encode(buffer); return buffer; }}());""".format(
				scriptUrl = scriptUrl, 
				baseVar = self._baseVarname,
				refUuid = uuid.uuid4()
				)
			respon = self._rawExecute(buffer)
		
		#응답받은 결과가 없으면 그대로 반환
		if respon is None:
			return None
		
		#function
		if respon['type'] == 'function':
			return Function(self, respon['refUuid'])
		
		#array
		if respon['type'] == 'array':
			return Array(self, respon['refUuid'])
		
		#object
		if respon['type'] == 'object':
			return Object(self, respon['refUuid'])
		
		#기본 타입
		return respon['value']
	