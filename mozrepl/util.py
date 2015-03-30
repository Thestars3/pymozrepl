#!/usr/bin/env python
#-*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import, division, print_function
import cookielib
#from ufp.terminal.debug import print_ as debug

def convertToJs(arg):
	"""
	입력받은 값을 javascript에서 사용 가능한 값으로 변환합니다.
	
	:param arg: 변환할 값
	:type arg: int, float, None, unicode, bytes, str, :py:class:`~mozrepl.type.Object`, :py:class:`~mozrepl.type.Function`, :py:class:`~mozrepl.type.Array`
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
	
	from ..type import Object
	if isinstance(arg, Object):
		return arg.reference
	
	raise TypeError('{}는 처리 할 수 없는 타입입니다.'.format(type(arg)))

def getCookiesFromHost(repl, host):
	"""
	:param repl: mozrepl.Mozrepl 객체
	:type repl: :py:class:`~mozrepl.Mozrepl`
	:param host: 호스트
	:type host: unicode
	:yield: 각 cookielib.Cookie.
	"""
	buffer = repl.execute('Services').cookies.getCookiesFromHost(host)
	for cookie in buffer:
		cookie = cookie.QueryInterface(repl.execute('Ci').nsICookie)
		
		domain = cookie.host
		initial_dot = domain.startswith(".")
		
		expires = cookie.expires
		if expires == 0:
			expires = None
		
		yield cookielib.Cookie(0, cookie.name, cookie.value, None, False, domain, cookie.isDomain, initial_dot, cookie.path, False, cookie.isSecure, expires, cookie.isSession, None, None, {})
	pass
