#!/usr/bin/env python
#-*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import, division, print_function
import cookielib

__all__ = ['getCookiesFromHost', 'convertToJs']

def convertToJs(arg):
	"""
	입력받은 값을 javascript에서 사용 가능한 값으로 변환합니다.
	
	:param arg: 변환할 값
	:type arg: int, float, None, unicode, bytes, str, :py:class:`~mozrepl.type.Object`, :py:class:`~mozrepl.type.Function`
	:return: javascript에서 사용 할 수 있는 값.
	:rtype: unicode
	"""
	if arg is None:
		return 'null'
	
	if isinstance(arg, (int, float)):
		return repr(arg)
	
	if isinstance(arg, unicode):
		return repr(arg.encode('UTF-8'))
	
	if isinstance(arg, str):
		return repr(arg)
	
	if isinstance(arg, Object):
		return arg.reference
	
	raise TypeError('{}는 처리 할 수 없는 타입입니다.'.format(type(arg)))

def getCookiesFromHost(repl, host):
	"""
	:param repl: mozrepl.Mozrepl 객체
	:type repl: mozrepl.Mozrepl
	:param host: 호스트
	:type host: unicode
	:yield: 각 cookielib.Cookie.
	"""
	repl.console('let enum_ = Services.cookies.getCookiesFromHost("%(host)s");' % locals())
	while repl.console('enum_.hasMoreElements();'):
		repl.console('var cookie = enum_.getNext().QueryInterface(Ci.nsICookie);')
		
		#cookie['isHttpOnly'] = c('cookie.isHttpOnly')
		#cookie['expiry'] = c('cookie.expiry')
		
		name = repl.console('cookie.name')
		value = repl.console('cookie.value')
		domain = repl.console('cookie.host')
		path = repl.console('cookie.path')
		secure = repl.console('cookie.isSecure')
		discard = repl.console('cookie.isSession')
		domain_specified = repl.console('cookie.isDomain')
		
		expires = repl.console('cookie.expires')
		if expires == 0:
			expires = None
		
		initial_dot = domain.startswith(".")
		yield cookielib.Cookie(0, name, value, None, False, domain, domain_specified, initial_dot, path, False, secure, expires, discard, None, None, {})
	pass
	