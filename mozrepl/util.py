#!/usr/bin/env python
#-*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import, division, print_function
import cookielib
#from ufp.terminal.debug import print_ as debug

from .exception import Exception as MozException

def convertToJs(arg):
	"""
	입력받은 값을 javascript에서 사용 가능한 값으로 변환합니다.
	
	.. todo:: dict 형태 변환 기능을 추가.
	
	:param arg: 변환할 값. 만약 list와 tuple타입을 인자로 준다면, 포함된 값은 :py:func:`~mozrepl.util.convertToJs` 함수가 변환 할 수 있는 값이어야 합니다.
	:type arg: int, float, None, unicode, bytes, str, tuple, list, :py:class:`~mozrepl.type.Object`, :py:class:`~mozrepl.type.Function`, :py:class:`~mozrepl.type.Array`
	:return: javascript에서 사용 할 수 있는 값.
	:rtype: unicode
	"""
	if arg is None:
		return 'null'
	
	if isinstance(arg, (int, float)):
		return unicode(arg)
	
	if isinstance(arg, unicode):
		return repr(arg.encode('UTF-8'))
	
	if isinstance(arg, str):
		return repr(arg)
	
	if isinstance(arg, (tuple, list)):
		buffer = map(convertToJs, arg)
		buffer = ', '.join(buffer)
		return '[{0}]'.format(buffer)
	
	from .type import Object
	if isinstance(arg, Object):
		return arg.reference
	
	raise TypeError('"{type}" 타입은 변환 할 수 없는 타입입니다.'.format(type=type(arg)))

def getCookiesFromHost(repl, host):
	"""
	host와 일치하는 쿠키를 cookielib.Cookie형식으로 가져옵니다.
	
	.. todo:: 버그 있음 수정 할 것.
	
	:param repl: mozrepl.Mozrepl 객체
	:type repl: :py:class:`~mozrepl.Mozrepl`
	:param host: 호스트
	:type host: unicode
	:yield: 각 cookielib.Cookie.
	"""
	repl.execute('{baseVar}.buffer = Services.cookies.getCookiesFromHost({host})'.format(baseVar=self._baseVarname, host=convertToJs(host)))
	while repl.execute('{baseVar}.buffer.hasMoreElements()'.format(baseVar=self._baseVarname)):
		cookie = "{baseVar}.buffer.getNext().QueryInterface(Ci.nsICookie)".format(baseVar=self._baseVarname)
		
		domain = cookie.host
		initial_dot = domain.startswith(".")
		
		expires = cookie.expires
		if expires == 0:
			expires = None
		
		yield cookielib.Cookie(0, cookie.name, cookie.value, None, False, domain, cookie.isDomain, initial_dot, cookie.path, False, cookie.isSecure, expires, cookie.isSession, None, None, {})
	pass
